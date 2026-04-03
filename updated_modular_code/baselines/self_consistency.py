from collections import Counter
import json
import re

debate = 1

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def self_consistency(llm, question, n_samples):
    """
    Self-Consistency baseline:
    - Sample the LLM 'n_samples' times
    - Extract answer from each response
    - Return the majority vote and all samples for logging
    # Fact Verification is either REFUTED or SUPPORTED. # The final answer will either be 'REFUTED' or 'SUPPORTED'. #
    """

    samples = []
    reasonings = []
    json_sc = "{\n\t\"answer\": \"REFUTED or SUPPORTED\",\n\t\"reasoning\": \" Concise explination of your reasoning for \"answer\"\"\n}"
    for _ in range(n_samples):

        prompt = f"""
You must answer only in valid JSON. No extra text.

Question:
{question}

Provide reasoning separately in 'reasoning:'.

Return JSON only:

{json_sc}

Rules:
- Output MUST be valid JSON (parsable with json.loads)
- "answer" must be either REFUTED or SUPPORTED.
- "answer" must be one word.
- Do not include any text before json.
- Do NOT include <think> or hidden reasoning
- "reasoning" cannot be more than 8 sentences.

Return only json.
"""
        #print(prompt)
        # Use query(), not generate()
        response = llm.query(prompt)
        print(f"Self Consistency: {debate}")
        try:
            clean = extract_json(response)

            if not clean:
                raise ValueError("No JSON found")
            parsed = json.loads(clean)
            #parsed = json.loads(response)

            answer = parsed.get("answer", "UNKNOWN")
            reasoning = parsed.get("reasoning", "")

            samples.append(answer)
            reasonings.append(reasoning)

        # Add additional queries.
        except Exception:
            # Attempt 2
            print("ERROR: Prompting attempt 2")
            response = llm.query(prompt)

            try:
                clean = extract_json(response)

                if not clean:
                    raise ValueError("No JSON found")
                parsed = json.loads(clean)
                #parsed = json.loads(response)

                answer = parsed.get("answer", "UNKNOWN")
                reasoning = parsed.get("reasoning", "")

                samples.append(answer)
                reasonings.append(reasoning)

            # Attempt 3
            except Exception:
                # Attempt 3
                print("ERROR: Prompting attempt 3")
                response = llm.query(prompt)

                try:
                    clean = extract_json(response)

                    if not clean:
                        raise ValueError("No JSON found")
                    parsed = json.loads(clean)
                    #parsed = json.loads(response)

                    answer = parsed.get("answer", "UNKNOWN")
                    reasoning = parsed.get("reasoning", "")

                    samples.append(answer)
                    reasonings.append(reasoning)

                # Failsafe
                except Exception:
                    print("ERROR: Passing \"NULL\" value")
                    samples.append("NULL")
                    reasonings.append("ERROR: REASONING NOT FORMATTED CORRECTLY")
            """
            # Extract the answer
            a1 = "\"answer\""
            r1 = "\"reasoning\""
            answer = "NULL"
            print(response)
            if a1 in response:
                answer = response.split(a1)[1].split("\n")[0].strip()
                if r1 in response:
                    reasoning = response.split(r1)[1].split("\n")[0].strip()
                    reasonings.append(reasoning)
                else:
                    reasonings.append("ERROR: REASONING NOT FORMATTED CORRECTLY")
            else:
                answer = response.strip()
                reasonings.append("ERROR: REASONING NOT FORMATTED CORRECTLY")

            samples.append(answer)
            #reasonings.append(reasoning)
            """
    # Take majority vote
    #majority_vote = Counter(samples).most_common(1)[0][0]

    # UPDATED MAJORITY VOTE
    counts = Counter(samples)
    most_common = counts.most_common()

    # Check if top two counts are equal (tie case)
    if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
        majority_vote = "NULL"
    else:
        majority_vote = most_common[0][0]

    globals()["debate"] += 1
    self_consistency_results = {

        "final_verdict": majority_vote,
        "verdicts": samples,
        "reasonings": reasonings

    }

    return self_consistency_results
