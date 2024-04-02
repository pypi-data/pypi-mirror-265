# powerline-wttr
- A Powerline segment for displaying weather information from wttr.in

# Installation
```
pip3 install powerline-wttr
```

# Configuration
- Add the following to your powerline configuration file:
- The `city` argument is the city to get the weather for.
- The `format` argument is the format string to use(Optional).
```json
{
    "function": "powerline_wttr.weather",
    "priority": 100,
    "args": {
        "city": "Tokyo",
        "format": "%l:+%c+%f+%h+%p+%P+%m+%w" 
    }
}
```
