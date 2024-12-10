import sqlite3
import xlsxwriter

workbook = xlsxwriter.Workbook('Report.xlsx')
worksheet = workbook.add_worksheet()
con = sqlite3.connect("airplanes.db")

year = int(input("Введите год: "))

bold = workbook.add_format({'bold': True})
header = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center'})
bottom_border = workbook.add_format({'bottom': 1})

row = 1
col = 0
total_sum = 0

routes = con.execute("SELECT id, ticket_price_rub FROM routes WHERE id IN (SELECT route FROM flights)")
for route_id, price in routes.fetchall():
    row += 1
    worksheet.write(row, col, f"Номер маршрута: {route_id}")
    worksheet.write(row, col + 1, f"Цена билета: {price}")
    row += 1
    worksheet.write(row, col, "Номер рейса", header)
    worksheet.write(row, col + 1, "Число пассажиров рейса", header)
    worksheet.write(row, col + 2, "Прибыль от полета, руб.", header)
    flights = con.execute(
        f"""SELECT id FROM flights WHERE route = {route_id} AND (departure_time BETWEEN "{year}-01-01 00:00:00" AND "{year}-12-31 23:59:59")""")
    route_sum = 0
    for flight_id in flights.fetchall():
        row += 1
        passengers_count = int(con.execute(
            f"SELECT COUNT(*) FROM passengers_has_flights WHERE flights_flight_id = {flight_id[0]}").fetchone()[0])
        worksheet.write(row, col, flight_id[0])
        worksheet.write(row, col + 1, passengers_count)
        worksheet.write(row, col + 2, passengers_count * price)
        route_sum += passengers_count * price
    row += 1
    worksheet.write(row, col, "Итого по маршруту, руб.:", bottom_border)
    worksheet.write(row, col + 2, route_sum)
    total_sum += route_sum

row += 1
worksheet.write(row, col, "Итого, руб.:", bold)
worksheet.write(row, col + 2, total_sum, bold)

worksheet.autofit()
worksheet.merge_range("A1:C1", f"Прибыль от маршрутов авиакомпании за {year} год", header)

workbook.close()
