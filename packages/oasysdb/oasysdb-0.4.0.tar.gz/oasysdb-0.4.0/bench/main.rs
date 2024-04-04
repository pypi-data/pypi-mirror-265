mod utils;

use criterion::*;
use oasysdb::prelude::*;
use utils::*;

fn build_collection(path: &str) -> Collection {
    let records = get_records(path).unwrap();
    let config = Config::default();
    Collection::build(&config, &records).unwrap()
}

fn bench_search_collection(criterion: &mut Criterion) {
    let id = "Search collection";

    // Download the dataset.
    download_siftsmall().unwrap();

    // Load the query data.
    let query_path = "data/siftsmall/siftsmall_query.fvecs";
    let query_data = read_vectors(query_path).unwrap();
    let vector: Vector = query_data[0].clone().into();

    // Create the collection.
    let base_path = "data/siftsmall/siftsmall_base.fvecs";
    let collection = build_collection(base_path);

    // Benchmark the search speed.
    let routine = || {
        black_box(collection.search(&vector, 10).unwrap());
    };

    criterion.bench_function(id, |bencher| bencher.iter(routine));
}

criterion_group!(bench, bench_search_collection);
criterion_main!(bench);
