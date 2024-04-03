if __name__ == "__main__":
    # lm = get_huggingface_lm(
    #    "Salesforce/instructcodet5p-16b",
    #    precision=torch.float16,
    #    trust_remote_code=True,
    # )
    # print(lm._model.config)
    # print(lm._model.config.encoder.n_positions)
    # print(lm.token_limit)

    # Use a pipeline as a high-level helper
    from transformers import pipeline

    user = (
        "In Bash, how do I list all text files in the current directory (excluding"
        " subdirectories) that have been modified in the last month?"
    )

    instr_prompt1 = f"<s>[INST] {user.strip()} [/INST]"

    pipe = pipeline("text-generation", model="codellama/CodeLlama-7b-Instruct-hf")
    print(pipe.predict(instr_prompt1))
