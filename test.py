 # 1. Submit a batch (POST /api/beta/batches).
                created = requests.post(
                    "https://openrouter.ai/api/beta/batches",
                    headers={**HEADERS, "Content-Type": "application/json"},
                    json={
                        "endpoint": "/v1/chat/completions",
                        "model": "openai/gpt-6-astra",
                        "requests": [
                            {
                                "custom_id": "request-1",
                                "body": {
                                    "model": "openai/gpt-6-astra",
                                    "messages": [{"role": "user", "content": answer}],
                                },
                            }
                        ],
                    },
                ).json()
                batch_id = created["id"]

                # 2. Poll GET /api/beta/batches/:id until the batch is terminal — "results" are inlined.
                #    Batch inputs and results are retained for 30 days.
                while True:
                    batch = requests.get(
                        f"https://openrouter.ai/api/beta/batches/{batch_id}",
                        headers=HEADERS,
                    ).json()
                    if batch["status"] in ("completed", "failed", "cancelled", "expired"):
                        break
                    time.sleep(10)

                print(batch["status"], batch["results"])
                # response = client.responses.create(model="gpt-6-astra",input=answer)
                # # response = client.responses.create(model="gpt-5.6-mini",input=answer)
                # print(20,response)
                # # response = client.responses.create(model="gpt-5.6-luna",input=answer)
                # response1 = client.responses.create(model="gpt-6-astra",input=answer)
                # print(11,response1)
                # context={
                # 'answer':response,
                # }