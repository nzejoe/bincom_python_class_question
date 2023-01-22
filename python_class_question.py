import random
import psycopg2
import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup

load_dotenv()
print(os.environ.get("DATABASE_PASSWORD"))

# open the html file
with open("python_class_question.html") as html_file:
    soup = BeautifulSoup(html_file, "lxml")  # parse the html file with lxml

# print(soup.prettify())

weekly_colors = list()
# get all the week days
week_days = soup.find_all("tr")

for day in week_days:
    day_colors = day.find_all("td")
    day_name = day_colors[0].text

    daily_colors = day_colors[1].text.strip()
    daily_colors = daily_colors.split(",")

    color_values = list()
    for color in daily_colors:
        color = color.strip()
        weekly_colors.append(color)

# count dress color appearance for the week
color_counter = dict()
for color in weekly_colors:
    color_counter[color] = color_counter.get(color, 0) + 1
print(color_counter)

count_list = list()
most_count = 0
most_worn_color = None

for color, count in color_counter.items():
    count_list.append(count)

    # get the most worn color for the week
    if count > most_count:
        most_count = count
        most_worn_color = color


def cal_median(nums):
    """
    this function accept a list of numbers,
    calculate and return the median
    """
    median = None
    # arrange nums from lowest to high
    nums.sort()
    count = len(nums)
    # foor of count / 2
    count_floor = count // 2
    if count % 2 == 0:
        median = (nums[count_floor - 1] + nums[count_floor]) / 2
    else:
        median = nums[count_floor]
    return median


def get_variants(list_items):
    """
    this function generates all shirt color variants
    """
    distint_list = []
    for item in list_items:
        if item in distint_list:
            continue
        distint_list.append(item)
    return distint_list


def generate_nums():
    """
    this function  generates random 4 digits number of 0s and 1s
    and convert the generated number to base 10.
    """
    generated = []
    while len(generated) < 4:
        rand_num = random.randint(0, 1)
        if len(generated) == 0 and rand_num == 0:
            continue
        generated.append(rand_num)

    # convert to base 10
    generated = "".join(map(str, generated))
    base10 = sum(int(b) * 2**i for i, b in enumerate(reversed(generated)))

    return [generated, base10]


def sum_fibonacci_sequence():
    """
    this function responsible for summing up the first 50 fibonacci sequence
    """
    x, y = 0, 1
    total = 0
    while y < 50:
        total += y
        x, y = y, x + y

    print(f"9. The sum of fibonacci secquence of first 50: \n\t {total}\n")


def save_color_frequencies():
    """
    this function is responsible for saving color
    frequencies to postgresql databse.
    for this to work, you must create a postgresql database locally.
    """
    # establishing the connection
    try:
        conn = psycopg2.connect(
            database="shirt_data",
            user="postgres",
            password=os.environ.get("DATABASE_PASSWORD"),
            host="127.0.0.1",
            port="5432",
        )
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        print("Connection established to: ", data)

        # if shirt_colors table already exists drop and then create table again
        commands = (
            """
                DROP TABLE IF EXISTS shirt_colors;
            """,
            """
                CREATE TABLE shirt_colors (
                    id SERIAL PRIMARY KEY,
                    color VARCHAR(20),
                    frequency INT
                )
            """,
        )

        for command in commands:
            cursor.execute(command)
        print("Table created successfully!")

        # insert all colors and their frequencies to shirt_color table
        for color, count in color_counter.items():
            insert_colors = f"""
                INSERT INTO shirt_colors (color,frequency)
                values('{color}',{count})
            """
            cursor.execute(insert_colors)
        print("Colors inserted...")

        cursor.close()
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn is not None:
            conn.close()


# print("\nMy print:", generate_nums())

mean_color = format(sum(count_list) / len(count_list), ".2f")
print(f"1. Mean color is: \n\t {mean_color}\n")
print(f"2. Most worn color is: \n\t {most_worn_color}: {most_count}\n")
print(f"3. The median is: \n\t {cal_median(count_list)}\n")
print(f"4. The color variance are: \n\t")
for color in get_variants(weekly_colors):
    print(color)
print()
print(
    f"8. Generated 4 numbers to base 10: \n\t {generate_nums()[0]} = {generate_nums()[1]}\n"
)

sum_fibonacci_sequence()
# call function to save color frequencies to database
save_color_frequencies()
