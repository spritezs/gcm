
if [ -z "$1" ]; then
  echo "Error: Model name must be passed as an argument."
  echo "Usage: bash solve.sh <model_name>"
  exit 1
fi
MODEL_TYPE="$1"
export MODEL_TYPE

# ONLY RUN THIS FOR ONE MODEL AT A TIME. CANT RUN MANY MODELS IN PARALLEL

find ./Params/*.param | parallel '
    param_file={};
    param_name=$(basename "$param_file" .param)
    echo "Processing parameter file: $param_name"

    # Create a unique output directory for each parallel task
    output_dir="./output/conjure-output-${MODEL_TYPE}-${param_name}";
    rm -rf "$output_dir"
    mkdir -p "$output_dir";

    conjure --output-directory="$output_dir" ./Models/${MODEL_TYPE}.essence -ac

    conjure translate-parameter --eprime "$output_dir"/model000001.eprime --essence-param "$param_file" --eprime-param "$output_dir"/eprime.params

    python modify_model.py "$param_name" "$output_dir" "$MODEL_TYPE"
    cp ./${MODEL_TYPE}-final/rel_dom.essence "$output_dir"

    ../conjure-oxide/target/release/conjure-oxide solve --no-use-expand-ac  --output ${output_dir}/sols.json  ${output_dir}/${MODEL_TYPE}.eprime

    if [[ "$MODEL_TYPE" == "RC" ]]; then
        python filter_dominant_solutions_RC.py "$output_dir"
    elif [[ "$MODEL_TYPE" == *"SRC"* ]]; then
        python filter_dominant_solutions_SRC.py "$output_dir"
    else
        echo "Error: Unknown model type: $MODEL_TYPE"
        exit 1
    fi

    # # # --human-rule-trace=trace.txt

    mv "$output_dir"/non-dominated.json "./Solutions/${param_name}_${MODEL_TYPE}_non-dominated.json"
'



