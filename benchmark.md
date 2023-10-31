## Single Thread

Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.46ms  781.04us  11.63ms   89.30%
    Req/Sec     1.05k    71.21     2.11k    95.52%
  299984 requests in 30.00s, 371.34MB read
Requests/sec:   9999.93
Transfer/sec:     12.38MB

## Threading

Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     8.42s     2.42s   12.61s    57.56%
    Req/Sec   582.45      4.36   588.00     75.00%
  174136 requests in 30.00s, 215.56MB read
Requests/sec:   5804.51
Transfer/sec:      7.19MB

## Thread Pool

Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     7.05s     2.19s   11.08s    56.64%
    Req/Sec   628.33     41.89   693.00     66.67%
  189740 requests in 30.00s, 234.87MB read
Requests/sec:   6324.95
Transfer/sec:      7.83MB

## Async

Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   244.92ms   43.78ms 328.45ms   67.17%
    Req/Sec     0.99k    44.29     1.06k    75.80%
  297034 requests in 30.00s, 367.69MB read
Requests/sec:   9901.95
Transfer/sec:     12.26MB
