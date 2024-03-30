use clap::Parser;
use log::{error, info};
use routee_compass::app::compass::compass_app::CompassApp;
use routee_compass::app::compass::compass_app_args::CompassAppArgs;
use routee_compass::app::compass::compass_app_error::CompassAppError;
use routee_compass::app::compass::compass_json_extensions::CompassJsonExtensions;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;

fn main() -> Result<(), Box<dyn Error>> {
    env_logger::init();

    // build CompassApp from config
    let args = CompassAppArgs::parse();

    let conf_file = args.config.ok_or_else(|| {
        CompassAppError::NoInputFile("No configuration file specified".to_string())
    })?;

    let compass_app = match CompassApp::try_from(conf_file.as_path()) {
        Ok(app) => app,
        Err(e) => {
            error!("Could not build CompassApp from config file: {}", e);
            return Err(Box::new(e));
        }
    };

    // read user file containing JSON query/queries
    let query_file = File::open(args.query_file.clone()).map_err(|_e| {
        CompassAppError::NoInputFile(format!(
            "Could not find query file {}",
            args.query_file.display()
        ))
    })?;
    let reader = BufReader::new(query_file);
    let user_json: serde_json::Value =
        serde_json::from_reader(reader).map_err(CompassAppError::CodecError)?;
    let user_queries = user_json.get_queries()?;
    info!("Query: {:?}", user_json);

    let run_config = match args.run_config {
        Some(run_config_path) => {
            let f = File::open(run_config_path)?;
            let r = std::io::BufReader::new(f);
            let j: serde_json::Value = serde_json::from_reader(r)?;
            Some(j)
        }
        None => None,
    };

    let results = compass_app.run(user_queries, run_config.as_ref())?;

    // scan the results and log any json values that have "error" in them
    for result in results.iter() {
        if let Some(error) = result.get("error") {
            let error_string = error.to_string().replace("\\n", "\n");
            error!("Error: {}", error_string);
        }
    }

    Ok(())
}
