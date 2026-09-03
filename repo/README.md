# solar-lead-capture-agent

An open-source reference implementation of a 24/7 AI voice agent that captures solar and roofing
leads: answers inbound calls, qualifies prospects by your criteria, and books estimates on your
calendar. Built by [ConvertX Ops](https://convertxops.vercel.app).

> Not a hosted product. This repo is the blueprint + a runnable demo so installers and developers
> can see exactly how the capture pipeline works. The managed version (with 100 free test calls)
> is at convertx.ops@gmail.com.

## What it does
1. Inbound call webhook -> transcribe (Whisper, local/OSS)
2. LLM qualifies via your criteria (roof type, service area, timeline, budget)
3. Books a calendar slot via Cal.com / Google Calendar API
4. Logs the lead + sends a summary to your CRM / email

## Stack (all free / open-source)
- Transcription: [whisper.cpp](https://github.com/ggerganov/whisper.cpp) or faster-whisper
- LLM: any OpenAI-compatible local model (Ollama + Qwen2.5 / Mistral)
- Telephony: Twilio (free trial) or a SIP trunk
- Calendar: Cal.com (self-hosted, free)
- Orchestration: Python

## Quick start
```bash
pip install -r requirements.txt
cp .env.example .env   # add your keys
python agent.py
```

## Why this exists
Most solar/roofing businesses lose high-intent enquiries to slow or missed after-hours calls.
A $7k lead that hits voicemail at 8pm calls your competitor. This agent answers in <1s and books
the estimate while intent is hot.

## License
MIT — use it, fork it, deploy it.
