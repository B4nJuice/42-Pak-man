from .config import ConfigManager

def main():
    # config: ConfigManager = ConfigManager('test.json')
    ConfigManager('test.jsonc')
    print("Hello from pak-man!")


if __name__ == "__main__":
    main()
