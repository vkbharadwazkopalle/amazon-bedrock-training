/// Simple line‑by‑line diff algorithm.
/// Lines that differ are prefixed with "-" for the first file and "+" for the second.
pub fn line_diff(a: &str, b: &str) -> Vec<String> {
    let a_lines: Vec<&str> = a.lines().collect();
    let b_lines: Vec<&str> = b.lines().collect();
    let mut result = Vec::new();
    let max = std::cmp::max(a_lines.len(), b_lines.len());
    for i in 0..max {
        let line_a = a_lines.get(i).copied();
        let line_b = b_lines.get(i).copied();
        match (line_a, line_b) {
            (Some(a), Some(b)) if a == b => {
                result.push(format!("  {}", a));
            }
            (Some(a), Some(b)) => {
                result.push(format!("- {}", a));
                result.push(format!("+ {}", b));
            }
            (Some(a), None) => {
                result.push(format!("- {}", a));
            }
            (None, Some(b)) => {
                result.push(format!("+ {}", b));
            }
            _ => {}
        }
    }
    result
}
