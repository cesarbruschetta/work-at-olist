# API to Register Call and Telephone Bill

## End Points

* `POST /api/call/` - Registe to start or end from call
* `GET  /api/billing/:telephone_number/` - Return history calls of last month or to period infromed

## Examples of requisitions of Call

### Register start call

```json
{
  "type":  "start",
  "timestamp": "2018-12-18T21:57:13Z",
  "call_id":  1,
  "source":  "1122345678",
  "destination":  "11999998888"
}
```

### Register end  call

```json
{
  "type":  "end",
  "timestamp": "2018-12-18T22:04:13Z",
  "call_id":  1
}
```

## Examples of return of billing

* `GET  /api/billing/1122345678/?month=12&year=2017`
*  Examples return

```json
{
    "telephone": "1122345678",
    "period": "12/2017",
    "calls": [
        {
            "destination": "9933468278",
            "call_start_date": "2017-12-11",
            "call_start_time": "15:07:13",
            "format_duration": "0h7m43s",
            "price": 0.99
        },
        {
            "destination": "9933468278",
            "call_start_date": "2017-12-12",
            "call_start_time": "22:47:56",
            "format_duration": "0h3m0s",
            "price": 0.36
        },
        ...
    ]
}
```

