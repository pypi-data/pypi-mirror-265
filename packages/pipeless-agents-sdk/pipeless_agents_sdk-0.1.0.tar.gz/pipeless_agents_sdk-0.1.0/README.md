# Python SDK for Pipeless Agents

Pipeless Agents converts any video feed into an actionable data stream that you can easily process. It allows you to build AI vision powered applications effortlessly. You just need to work with JSON data as you usually do.

Configure your video sources in the [Dashboard](https://agents.pipeless.ai) and then use this SDK to process the data stream.

## SDK Usage

```
from pipeless_agents_sdk.cloud import data_stream

for payload in data_stream:
  print(f"New data received: {payload.value}
  // process the received data here
```

That's all!
