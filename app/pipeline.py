import json
from .kafka_io import make_consumer, make_producer, produce_json
from . import config
from .enrichers import search_linkedin_url, fetch_linkedin_profile
from .llm_chain import make_llm, run_icebreaker

def main():
    consumer = make_consumer()
    producer = make_producer()
    llm = make_llm()

    print(f"Consuming from {config.INPUT_TOPIC} ...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue

        try:
            lead = json.loads(msg.value().decode("utf-8"))
            full_name = lead.get("full_name")
            company = lead.get("company")
            print(f"\nLead: {full_name} / {company}")

            url = search_linkedin_url(full_name, company)
            if url:
                print("LinkedIn URL:", url)
                profile = fetch_linkedin_profile(url)
            else:
                profile = {}

            result = run_icebreaker(llm, json.dumps(profile), full_name, company)
            print("Icebreakers ready.")

            output = {
                "full_name": full_name,
                "company": company,
                **result
            }

            produce_json(producer, config.OUTPUT_TOPIC, output)
            print("Produced enriched data to", config.OUTPUT_TOPIC)

        except Exception:
            print("Processing error: skipping this lead")

if __name__ == "__main__":
    main()
