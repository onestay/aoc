test_data = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen"
]

letter_digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine":9}
longest_letter_digit = 5

def extract_numbers(line: str) -> int:
    n1 = None
    n2 = None
    current_letter_digit = ""
    first_letter_digit_position = 0
    i = 0
    while i < len(line):
        char = line[i]
        if char.isdigit():
            if len(current_letter_digit) != 4:
                current_letter_digit = ""
                if n1 is None:
                    n1 = int(char)
                else:
                    n2 = int(char)
                i += 1
                continue
            else:
                current_letter_digit = ""
                i = first_letter_digit_position + 1
        else:
            if len(current_letter_digit) == 0:
                first_letter_digit_position = i
            current_letter_digit += char
            if current_letter_digit in letter_digits:
                if n1 is None:
                    n1 = letter_digits[current_letter_digit]
                else:
                    n2 = letter_digits[current_letter_digit]
                current_letter_digit = ""
                i = first_letter_digit_position + 1
                continue
            if len(current_letter_digit) == 5:
                current_letter_digit = ""
                i = first_letter_digit_position + 1
                continue
            i += 1
            

    if n1 is None:
        raise Exception(f"{line} has no int")
    if n2 is None:
        n2 = n1
    return n1 * 10 + n2

n = 0
for line in open("input"):
    tmp = extract_numbers(line)
    print(f"{line} {tmp}")
    n += tmp

print(n)