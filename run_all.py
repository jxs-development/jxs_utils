import encoder_test
import decoder_test

decoder_test_result, decoder_bad_list = decoder_test.main()
encoder_test_result, encoder_bad_list = encoder_test.main()
 

print("encoder_test: ", encoder_test_result, "decoder_test: ", decoder_test_result)

if not encoder_test_result:
    print("[------ encoder bad list ------]")
    for bad_info in encoder_bad_list:
        print(bad_info)

if not decoder_test_result:
    print("[------ decoder bad list ------]")
    for bad_info in decoder_bad_list:
        print(bad_info)
