use actix_web::{middleware, web, App, HttpServer};
use std::io::Write;

mod handlers;
mod diff;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Simple logger
    env_logger::init();

    HttpServer::new(|| {
        App::new()
            .wrap(middleware::Logger::default())
            .service(web::resource("/compare").route(web::post().to(handlers::compare_files)))
            .service(web::resource("/").route(web::get().to(handlers::index)))
            .service(actix_files::Files::new("/static", "static").show_files_listing())
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
