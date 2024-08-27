import time
import random

def get_sample_text():
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs.",
        "How razorback-jumping frogs can level six piqued gymnasts!",
        "Sphinx of black quartz, judge my vow.",
        "The five boxing wizards jump quickly."
    ]
    return random.choice(texts)

def typing_speed_test():
    sample_text = get_sample_text()
    print("Typing Speed Test")
    print("-----------------")
    print("Type the following text as quickly and accurately as you can:")
    print()
    print(sample_text)
    print()
    
    input("Press Enter when you are ready to start...")

    start_time = time.time()
    typed_text = input("Start typing here: ")
    end_time = time.time()

    elapsed_time = end_time - start_time
    words_typed = len(typed_text.split())
    words_per_minute = (words_typed / elapsed_time) * 60

    print()
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Words typed: {words_typed}")
    print(f"Words per minute: {words_per_minute:.2f}")

    if typed_text == sample_text:
        print("You typed the text correctly!")
    else:
        print("You made some mistakes in typing the text.")

if __name__ == "__main__":
    typing_speed_test()

