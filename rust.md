# Working on Rust project cheat sheet

## Faster linking

### Linux

- Install linker

        sudo apt-get install lld clang

- Create a `.cargo/config.toml` file with 

        [target.x86_64-unknown-linux-gnu]
        rustflags = ["-C", "linker=clang", "-C", "link-arg=-fuse-ld=lld"]

### MacOS

- Install linker

        brew install llvm

    > follow steps in: `brew info llvm`

- Create a `.cargo/config.toml` file with 

        [target.x86_64-apple-darwin]
        rustflags = ["-C", "link-arg=-fuse-ld=lld"]
        [target.aarch64-apple-darwin]
        rustflags = ["-C", "link-arg=-fuse-ld=/opt/homebrew/opt/llvm/bin/ld64.ll

## Continuous check

To avoid running the cargo check / cargo run.

    cargo install cargo-watch

To monitor source code to trigger commands every time a file changes

    cargo watch -x check

We can chain as well (ex. run tests if check succeeds)

    cargo watch -x check -x test

## Continuous integration

### Running tests

    cargo test

> Note it builds the project beforehand

- With all the prints to the output

        cargo test -- --nocapture

### Code coverage

- Install

        cargo install cargo-tarpaulin

    If there is an OpenSSL error look at [linux packages](linux.md#useful-packages)

- Run

        cargo tarpaulin --ignore-tests

### Linting

- Install

        rustup component add clippy

- Run

        cargo clippy

- To fail when linter shows warnings, run

        cargo clippy -- -D warnings

- To mute warnings on the code block add

        #[allow(clippy::lint_name)]

- Linting may be done on the project level with 

        #![allow(clippy::lint_name)]

    Or in `clippy.toml`

### Formatting

- Install

        rustup component add rustfmt

- Run

        cargo fmt

- To fail in pipeline where not formated code present

        cargo fmt -- --check

- To tune formatting for the project

    We use the `rustfmt.toml`

### Security Vulnerabilities

We can check if vulnerabilities have been reported for any of the crates in the 
dependency tree of the project.

- Install

        cargo install cargo-audit

- Run

        cargo audit

### Setup a pipeline

#### Github

[Quickstart](https://docs.github.com/en/actions/quickstart)

[Example config](https://gist.github.com/LukeMathWalker/5ae1107432ce283310c3e601fac915f3)

#### Gitlab

[Quickstart](https://docs.gitlab.com/ee/ci/quick_start/)

[Example config](https://gist.github.com/LukeMathWalker/d98fa8d0fc5394b347adf734ef0e85ec)

#### CirckleCi

[Quickstart](https://circleci.com/docs/getting-started/)

[Example config](https://gist.github.com/LukeMathWalker/6153b07c4528ca1db416f24b09038fca)

## Packages Cargo.toml

To add dependencies like this:

```
[dependencies]
actix-web = "4"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

we can use commands

```
cargo add actix-web@4
cargo add tokio@1 --features macros,rt-multi-thread
```

To remove unused dependencies in the project

```
cargo install cargo-udeps
cargo +nightly udeps
```

> the output should be the list of unused imports

## Macros

### Show macros with `cargo expand`

Expands all macros in your code without passing the output to the compiler, allowing to step through it and understand what is going on.

- Install

        cargo install cargo-expand

- Run

        cargo expand

## Curl

[List of Curl options](https://gist.github.com/eneko/dc2d8edd9a4b25c5b0725dd123f98b10)

- GET request

        curl -v http://127.0.0.1:8000/health_check

> -v gives more response details

- POST request with `x-www-form-urlencoded` ver 1

        curl -i --header "Content-Type: application/x-www-form-urlencoded" --request POST http://127.0.0.1:8000/subscriptions -d "name=van%20Buren&email=armin_van_buren%40gmail.com"

- POST request with `x-www-form-urlencoded` ver 2

        curl -i -X POST http://127.0.0.1:8000/subscriptions -d "name=van%20Buren&email=armin_van_buren%40gmail.com"

## HTML forms

### application/x-www-form-urlencoded

The keys and values [in our form] are encoded in key-value tuples separated by ‘&’, with a ‘=’ between
the key and the value. Non-alphanumeric characters in both keys and values are percent encoded.

[HTML URL Encoding Reference](https://www.w3schools.com/tags/ref_urlencode.ASP)

## Actix web

[Extracting form data](https://actix.rs/docs/extractors/)

## Serialization: serde

Serde defines a set of interfaces. If you need support for a specific data format, you need to pull in another crate (e.g. serde_json for JSON or avro-rs for Avro).

If you want to implement a library to support serialisation for a new data format, you have to provide an implementation of the Serializer trait.

[Understanding serde](https://www.joshmcguigan.com/blog/understanding-serde/)

# Outputs

## Logging

Standard [log crate](https://docs.rs/log/latest/log/)

Simple [env_logger crate](hhttps://docs.rs/env_logger/latest/env_logger/)

- To start logging add to main:

        env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();

- Execute the application with one of LEVEL -> trace, debug, info, warn and error

        RUST_LOG=<LEVEL> cargo run


actix_web provides middleware `actix_web::middleware::Logger`

## Pretty printing

We can use `jq` for this.

        sudo apt-get install jq

Then we can run with the pipe

        cargo run | jq

Manually

        jq <<< {\"key\":\"value\"}


        output:

        {
          "key": "value"
        }

## Formatting output with bunyan

Install bunyan

        cargo install bunyan

Example command

        TEST_LOG=true cargo test health_check_works | bunyan

## Tracing

Add tracing

        cargo add tracing --features="log"

Tracing has a nice `tracing::instrument` macro wich creates a wrapper around the function.

Example:

```
#[tracing::instrument(
    name = "Adding a new subscriber",
    skip(form, db_connection_pool),
    fields(
        request_id = %Uuid::new_v4(),
        subscriber_email = %form.email,
        subscriber_name = %form.name
    )
)]
pub async fn subscribe(
    form: web::Form<FormData>,
    db_connection_pool: web::Data<PgPool>,
) -> HttpResponse {
    match insert_subscriber(&form, &db_connection_pool).await {
        Ok(_) => HttpResponse::Ok().finish(),
        Err(_) => HttpResponse::InternalServerError().finish(),
    }
}
```

> The `name` will be logged as an output string. The `skip` defines which arguments passed to wrapped function should not be logged. The `fields` define which parameters should be added to the span.

## Secrecy

Is used if we don't want secrets like passwords or personal information in logs. It masks Debug implementation: `println!("{:?}",
my_secret_string)` and outputs `Secret([REDACTED String])` instead of the actual secret value.

Add secrecy

        cargo add secrecy --features="serde"

Example:

        use secrecy::{ExposeSecret, Secret};

        #[derive(serde::Deserialize)]
        pub struct DatabaseSettings {
        pub username: String,
        pub password: Secret<String>,
        pub port: u16,
        pub host: String,
        pub database_name: String,
        }

Example to read:

        &configuration.database.connection_string().expose_secret()

