import math
import argparse


def months_to_years(months):
    if months > 12:
        if months % 12 == 0:
            return "{} years".format(int(months / 12))
        else:
            return "{} years and {} months".format(int(months // 12), int(months % 12))
    else:
        return "{} months".format(int(months))


def calc_overpayment(annuity_payment, periods, loan_principal):
    return annuity_payment * periods - loan_principal


def calc_periods(arguments):  # n
    loan_principal, annuity_payment, loan_interest = arguments
    periods = math.ceil(
        math.log((annuity_payment / (annuity_payment - loan_interest * loan_principal)), 1 + loan_interest))
    print("It will take {} to repay this loan!".format(months_to_years(periods)))
    return calc_overpayment(annuity_payment, periods, loan_principal)


def calc_loan_principal(arguments):  # p
    annuity_payment, periods, loan_interest = arguments
    loan_principal = math.ceil(annuity_payment / (
            (loan_interest * pow(1 + loan_interest, periods)) / (pow(1 + loan_interest, periods) - 1)
    ))
    print("Your loan principal = {}!".format(loan_principal))
    return calc_overpayment(annuity_payment, periods, loan_principal)


def calc_annuity_payment(arguments):  # a
    loan_principal, periods, loan_interest = arguments
    annuity_payment = math.ceil(loan_principal * (
            loan_interest * pow(1 + loan_interest, periods) / (pow(1 + loan_interest, periods) - 1)
    ))

    print("Your annuity payment = {}!".format(annuity_payment))
    return calc_overpayment(annuity_payment, periods, loan_principal)


def calc_differentiate(arguments):
    loan_principal, periods, interest = arguments
    total_payment = 0
    for m in range(1, periods + 1):
        ith_payment = math.ceil(loan_principal / periods
                                + interest * (loan_principal - (loan_principal * (m - 1)) / periods))
        print("Month {}: payment is {}".format(m, ith_payment))
        total_payment += ith_payment
    return total_payment - loan_principal


def invalid_arguments(arguments):
    counter = 0
    for i in range(len(arguments)):
        if arguments[i] is not None:
            counter += 1
            if i > 0 and float(arguments[i]) < 0:
                return True
    if counter == 4:
        return False
    else:
        return True


parser = argparse.ArgumentParser()

parser.add_argument("--type")
parser.add_argument("--principal")
parser.add_argument("--payment")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()
arg_list = [args.type, args.principal, args.payment, args.periods, args.interest]

if args.interest is None or invalid_arguments(arg_list):
    print("Incorrect parameters")
else:
    arg_list = [int(args.principal) if args.principal is not None else None, int(args.payment) if args.payment is not None else None,
                int(args.periods) if args.periods is not None else None, float(args.interest)/1200.0]
    if args.type is None:
        print("Incorrect parameters")
    else:
        if args.type == "annuity":
            if args.principal is None:
                overpayment = calc_loan_principal(arg_list[1:])
            elif args.payment is None:
                overpayment = calc_annuity_payment([arg_list[0], arg_list[2], arg_list[3]])
            elif args.periods is None:
                overpayment = calc_periods([arg_list[0], arg_list[1], arg_list[3]])
        elif args.type == "diff":
            if args.payment is not None:
                print("Incorrect parameters")
            else:
                overpayment = calc_differentiate([arg_list[0], arg_list[2], arg_list[3]])

        print("Overpayment = ", overpayment)
