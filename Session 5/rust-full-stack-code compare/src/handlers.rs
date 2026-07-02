use actix_multipart::Multipart;
use actix_web::{HttpResponse, Responder};
use futures_util::StreamExt as _;
use serde::Serialize;
use std::io::Write;

use crate::diff::line_diff;

#[derive(Serialize)]
struct DiffResponse {
    diff: Vec<String>,
}

pub async fn index() -> impl Responder {
    // Serve a simple HTML page
    let html = r#"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Comparator</title>
</head>
<body>
    <h1>Compare Two Text Files</h1>
    <form id="form" enctype="multipart/form-data" method="post" action="/compare">
        <label>File 1: <input type="file" name="file1" required></label><br><br>
        <label>File 2: <input type="file" name="file2" required></label><br><br>
        <button type="submit">Compare</button>
    </form>
    <pre id="output"></pre>
    <script>
        const form = document.getElementById('form');
        const output = document.getElementById('output');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const res = await fetch('/compare', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            output.textContent = data.diff.join('\n');
        });
    </script>
</body>
</html>
"#;
    HttpResponse::Ok().content_type("text/html; charset=utf-8").body(html)
}

pub async fn compare_files(mut payload: Multipart) -> impl Responder {
    let mut files: Vec<Vec<u8>> = Vec::new();

    while let Some(item) = payload.next().await {
        let mut field = item.unwrap();
        let mut data = Vec::new();
        while let Some(chunk) = field.next().await {
            data.extend_from_slice(&chunk.unwrap());
        }
        files.push(data);
        if files.len() == 2 {
            break;
        }
    }

    if files.len() != 2 {
        return HttpResponse::BadRequest().body("Two files required");
    }

    let text1 = String::from_utf8_lossy(&files[0]);
    let text2 = String::from_utf8_lossy(&files[1]);

    let diff = line_diff(&text1, &text2);
    let response = DiffResponse { diff };
    HttpResponse::Ok().json(response)
}
