use pyo3::prelude::*;

#[pyfunction]
fn get_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn assoc_obj(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_version, m)?)?;

    Ok(())
}
