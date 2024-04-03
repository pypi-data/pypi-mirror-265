def test_quick():
    from johnsnowlabs import nlp
    license = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMzNTY3OTksImlhdCI6MTcwMTczNDQwMCwidW5pcXVlX2lkIjoiZWYxOTQ3YWEtOTM5MC0xMWVlLTk2ZTktNDY3ZTc5NmJkODRlIiwic2NvcGUiOlsibGVnYWw6aW5mZXJlbmNlIiwibGVnYWw6dHJhaW5pbmciLCJmaW5hbmNlOmluZmVyZW5jZSIsImZpbmFuY2U6dHJhaW5pbmciLCJvY3I6aW5mZXJlbmNlIiwib2NyOnRyYWluaW5nIiwiaGVhbHRoY2FyZTppbmZlcmVuY2UiLCJoZWFsdGhjYXJlOnRyYWluaW5nIl19.Oawzk29TFNGrZ2fEcyjrzJaccbBzQT64_qPtXpDezM-QipQuM3Yn1Zyb33Ky99K1nvMY8G1secjoilRvVGS5RkBYc14IQ7IcdejSng5CDxBn8-2vg3NVrnpvfc4fqVeNozaDCOPqReCeZLCteFU_Up3mkgJPPcYmpXt9ZwO52Vbi6xnOOiJO-2mM2OFrqUugyM026s3FJ0bjf9J2-f-lbPTttlSyQt1olpFSMv9TJC5wOwKMsb4mvZisCZGwJnvnv1PLJ9FpEy_Xf0qqXKgvrO7u3JZEm64hVvyY8Yj64Vg0Rc9hR6KQk_fdQo0gwnHWBxyFtDOqceWqc60w1QFKBw'
    aws_access_key_id = 'AKIASRWSDKBGPSWLOIHO'
    aws_secret_access_key = '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'

    nlp.start(model_cache_folder="/app/model_cache",

              aws_access_key=aws_secret_access_key,
              aws_key_id=aws_access_key_id,
              visual=False,
              hardware_target='cpu')