import re

with open("mysql_script.txt", mode="r", encoding="utf8") as input_file:
    contents = input_file.read()
contents = contents[contents.find("CREATE TABLE"):contents.find("SET SQL_MODE")]
contents = contents.replace("`airlines`.", "")
contents = contents.replace(" INT ", " INTEGER ")
contents = contents.replace("\nENGINE = InnoDB", "")
auto_increments = re.findall("`(.+)` .+ AUTO_INCREMENT", contents)
# print(auto_increments)
for table_with_auto_increment in auto_increments:
    contents = contents.replace(f"""PRIMARY KEY (`{table_with_auto_increment}`)""", f"""PRIMARY KEY (`{table_with_auto_increment}` AUTOINCREMENT)""")
contents = contents.replace(" AUTO_INCREMENT", "")
contents = "\n".join((line for line in contents.split("\n") if "INDEX" not in line))
with open("sqlite_script.txt", mode="w", encoding="utf8") as output_file:
    output_file.write(contents)
print(contents)