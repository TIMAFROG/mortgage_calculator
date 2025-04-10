from math import log

from flask import Flask, request, render_template

from ERRORS import *

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['POST', 'GET'])
@app.route('/kalk1', methods=['POST', 'GET'])
def kalk1():
    if request.method == 'GET':
        return render_template('r_t_html.html', count=0, total=[0, 0, 0])
    elif request.method == 'POST':
        return run1(request)


def ret(count, db, error, overpayment, total):
    return render_template('r_t_html.html', count=count, db=db, error=error, overpayment=overpayment, total=total)


def run1(req):
    db, total, error = [], [0, 0, 0], ''
    try:
        if not req.form['sum'].isdigit():
            raise ErrorMortgageAmount('сумма ипотеки должена содержать только цифры')
        elif req.form['percent'].count('.') == 1 or req.form['percent'].count('.') == 0:
            if not req.form['percent'].replace('.', '', 1).isdigit() or float(req.form['percent']) > 100 or float(
                    req.form['percent']) < 0:
                raise PercentError('процент может содержать цифры от 1 до 100 и .')
        elif (not req.form['time'].isdigit()) or int(req.form['time']) >= 200:
            raise ErrorInYear('период времени должен содержать только цифры <= 200 или = 0')
        elif not req.form['cont'].isdigit():
            raise ErrorInitialFee('первоначальный взнос должен содержать только цифры и быть < суммы ипотеки')
        elif int(req.form['sum']) == 0:
            raise ZeroError('сумма ипотеки не должна равняться 0')
        elif float(req.form['percent']) == 0:
            raise ZeroError('процент не должен равняться 0')
        elif int(req.form['time']) == 0:
            raise ZeroError('период времени не должен быть = 0')
        elif len(req.form['sum']) > 10:
            raise ErrorLargeNumber('сумма ипотеки слишком длинная')
        elif int(req.form['cont']) == 0:
            raise ZeroError('первоначальный взнос не должен быть равен 0')
        # это сложные формулы
        mortgage = int(req.form['sum']) - int(req.form['cont'])
        mortgage_interest = float(req.form['percent'])

        if req.form['select'] == 'year':
            mortgage_term_in_months = int(req.form['time']) * 12
        else:
            mortgage_term_in_months = int(req.form['time'])
        month = 0
        if req.form['a_or_d'] == 'a':
            print('Аннуитетные')
            monthly_rate = mortgage_interest / 12 / 100
            total_rate = (1 + monthly_rate) ** mortgage_term_in_months
            payment_per_month = int(mortgage * monthly_rate * total_rate / (total_rate - 1))
            overpayment = payment_per_month * mortgage_term_in_months - mortgage
            while month < mortgage_term_in_months:
                month += 1
                interest_part_debt = mortgage * monthly_rate
                main_debt = payment_per_month - interest_part_debt
                mortgage = mortgage - main_debt
                total[0] += int(main_debt) + int(interest_part_debt)
                total[1] += int(main_debt)
                total[2] += int(interest_part_debt)
                db.append([str(int(month)), str(int(main_debt) + int(interest_part_debt)), str(int(main_debt)),
                           str(int(interest_part_debt)), str(int(mortgage))])
        else:
            print('Дифференцированные')
            main_payment = mortgage / mortgage_term_in_months
            while month != mortgage_term_in_months:
                month += 1
                interest_payment = mortgage * (mortgage_interest / 12) / 100
                mortgage -= main_payment
                total[0] += int(main_payment) + int(interest_payment)
                total[1] += int(main_payment)
                total[2] += int(interest_payment)
                db.append([str(int(month)), str(int(main_payment + interest_payment)), str(int(main_payment)),
                           str(int(interest_payment)), str(int(mortgage))])
            overpayment = total[2]
        print(db)

    except ErrorMortgageAmount as e:
        error = f"Ошибка! {e}"
        return ret(0, [], error, '', [0, 0, 0])
    except PercentError as e:
        error = f"Ошибка! {e}"
        return ret(0, [], error, '', [0, 0, 0])
    except ErrorInYear as e:
        error = f"Ошибка! {e}"
        return ret(0, [], error, '', [0, 0, 0])
    except ErrorInMonth as e:
        error = f"Ошибка! {e}"
        return ret(0, [], error, '', [0, 0, 0])
    except ErrorInitialFee as e:
        error = f"Ошибка! {e}"
        return ret(0, [], error, '', [0, 0, 0])
    except ZeroError as e:
        error = f"Ошибка! {e}"
        return ret(0, [], error, '', [0, 0, 0])
    if req.form['select'] == 'year':
        return ret(int(req.form['time']) * 12, db, '', int(overpayment), total)
    return ret(int(req.form['time']), db, '', int(overpayment), total)


@app.route('/kalk2', methods=['POST', 'GET'])
def kalk2():
    if request.method == 'GET':
        return render_template('r_p_html.html', count=0)
    elif request.method == 'POST':
        return run2(request)


def ret2(error, overpayment, years, months):
    return render_template('r_p_html.html', error=error, overpayment=overpayment, years=years, months=months)


def run2(req):
    try:
        if not req.form['sum'].isdigit():
            raise ErrorMortgageAmount('сумма ипотеки должна содержать только цифры')
        elif not req.form['percent'].isdigit() or int(req.form['percent']) > 100:
            raise PercentError('процент должен содержать только цифры < 100')
        elif not req.form['ejemes_plata'].isdigit() or int(req.form['ejemes_plata']) > \
                int(req.form['ejemes_plata']):
            raise ErrorMonthlyPayment('ежемесячный платеж должен содержать только цифры и быть < суммы ипотеки')
        elif not req.form['cont'].isdigit():
            raise ErrorInitialFee('первоначальный взнос должен содержать только цифры и быть < суммы ипотеки')
        elif int(req.form['sum']) == 0:
            raise ZeroError('сумма ипотеки не должна быть = 0')
        elif int(req.form['ejemes_plata']) == 0:
            raise ZeroError('процент не должен равняться 0')
        elif int(req.form['percent']) == 0:
            raise ZeroError('ежемесячный платеж не должен равняться 0')
        elif int(req.form['cont']) == 0:
            raise ZeroError('первоначальный взнос не должен быть равен 0')

        # это почти не сложные формулы
        mortgage = int(req.form['sum']) - int(req.form['cont'])
        mortgage_percentage = int(req.form['percent'])
        monthly_rate = mortgage_percentage / 12 / 100
        payment_per_month = int(req.form['ejemes_plata'])
        mortgage_term_in_months = log((payment_per_month / ((mortgage * monthly_rate) - payment_per_month)) *
                                      (-1), 1 + monthly_rate)
        overpayment = payment_per_month * mortgage_term_in_months - mortgage


    except ErrorMortgageAmount as e:
        error = f"Ошибка! {e}"
        return ret2(error, '', '', '')
    except PercentError as e:
        error = f"Ошибка! {e}"
        return ret2(error, '', '', '')
    except ErrorMonthlyPayment as e:
        error = f"Ошибка! {e}"
        return ret2(error, '', '', '')
    except ErrorInitialFee as e:
        error = f"Ошибка! {e}"
        return ret2(error, '', '', '')
    except ZeroError as e:
        error = f"Ошибка! {e}"
        return ret2(error, '', '', '')
    return ret2(error='', overpayment=str(int(overpayment)), years=str(int(mortgage_term_in_months / 12)),
                months=str(int(mortgage_term_in_months % 12)))


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
