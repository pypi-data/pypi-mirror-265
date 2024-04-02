""""
A request ID is a unique identifier for each request. We decided that we wanted to be able to search for both a unique action and an entire request chain, so we implemented the following model:

If a request comes in with no request ID, generate a unique one.
If a request comes in with a request ID, add a comma and add a unique one.
This allows the following request chain (which could have any number of requests in between them) go from this:

POST /cards/lost_and_stolen/
GET /cards/1234567890123456/
GET /accounts/123456/
DELETE /cards/1234567890123456/
POST /accounts/123456/card/

To this:

0dadb33f-ee15-470a-bfc8-5e35926793a5 POST /cards/lost_and_stolen/
0dadb33f-ee15-470a-bfc8-5e35926793a5,ac0eabbd-122f-491c-aacf-670d255eef3d GET /cards/1234567890123456/
0dadb33f-ee15-470a-bfc8-5e35926793a5,f2aab75e-719f-4a00-8d81-a1266cfb6a81 GET /accounts/123456/
0dadb33f-ee15-470a-bfc8-5e35926793a5,639832bf-111c-40ac-abed-bf93ae15c54d DELETE /cards/1234567890123456/
0dadb33f-ee15-470a-bfc8-5e35926793a5,68493175-8a39-421b-99e9-53e937fa5d12 POST /accounts/123456/card/

"""