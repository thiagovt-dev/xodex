# Antes (problemático):
client = OpenAI(api_key=cfg["openai"]["api_key"], base_url=cfg["openai"]["base_url"])

# Depois (funcional):
def get_client():
    global client
    if client is None:
        try:
            client = OpenAI(
                api_key=cfg["openai"]["api_key"],
                base_url=cfg["openai"]["base_url"]
            )
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            client = OpenAI(api_key=cfg["openai"]["api_key"])
    return client