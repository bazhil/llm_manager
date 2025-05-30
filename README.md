# llm_manager
SDK project for use different LLM

## Usage

Clone the repository
```commandline
git clone https://github.com/bazhil/llm_factory.git
```

Create .env
```commandline
cp .env.example .env
```

Fill variables in .env
```co
DEEPSEEK_API_KEY=
GIGA_CHAT_AUTH_KEY=
OLLAMA_HOST=
OLLAMA_MODEL=
YANDEX_GPT_FOLDER_ID=
YANDEX_GPT_API_KEY=
OPENAI_API_KEY=
```

Install requirements:
```commandline
pip install -r requirements.txt
```

Where:
```text
PROVIDER - name of target llm (ollama / deepseek / openai / yandex / gigachat)
DEEPSEEK_API_KEY - Deepseek API KEY
GIGA_CHAT_AUTH_KEY - GigaChat Auth Key
OLLAMA_HOST - host, where running ollama
OLLAMA_MODEL - model of using ollama
YANDEX_GPT_FOLDER_ID - Yandex GPT Folder ID
YANDEX_GPT_API_KEY - Yandex GPT API KEY
OPENAI_API_KEY - OpenAI API Key
```

## Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by the need for reusing unified LLM interface
