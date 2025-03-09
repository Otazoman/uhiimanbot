#!/bin/bash

# Function to display usage information
display_usage() {
    echo "Usage: $0 [--run-tests] [-h|--help]"
    echo "    --run-tests    Run tests with coverage"
    echo "    -h, --help     Display this usage information"
}


# Check if any arguments are provided
run_tests=false
if [[ $# -gt 0 ]]; then
    case "$1" in
        --run-tests)
            run_tests=true
            shift ;;
        -h|--help)
            display_usage
            exit 0 ;;
        *)
            echo "Error: Unrecognized argument '$1'"
            display_usage
            exit 1 ;;
    esac
fi


start_time=$(date +%s)

# Run tests with coverage
if $run_tests; then
    # Run tests with coverage
    coverage run --source=../libs -m unittest discover -s libs -p '*.py'
    coverage report

    coverage run --source=../uhiimanbot -m unittest discover -s uhiimanbot -p '*.py'
    coverage report
fi

# Files to be cleared
files=(
    "testmaterials/data/brogger_content.html"
    "testmaterials/data/interval_postcontent.txt"
    "testmaterials/data/mail.txt"
    "testmaterials/data/output.db"
    "testmaterials/data/trendword_content.html"
    "testmaterials/logs/app.log"
)

echo "clear work data"
for file in "${files[@]}"; do
    echo -n > "$file"
done

echo "clear database"
mongosh --quiet --eval '
    use test_cr_tohonokai;
    db.auth("testtohonokai", "password");
    db.rss_article.remove({});
'

echo "done"

end_time=$(date +%s)
execution_time=$((end_time - start_time))
echo "Script execution time: $execution_time seconds"
coverage report
