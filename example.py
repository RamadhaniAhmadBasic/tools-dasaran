# Python 3.10.6
# Import Module
import os
import textwrap

# Define Variable

fg_black_c   = "\033[30m"
fg_red_c     = "\033[31m" # ERROE color
fg_green_c   = "\033[32m" # SUCCESS color
fg_yellow_c  = "\033[33m" # WARNING color
fg_blue_c    = "\033[34m"
fg_magenta_c = "\033[35m"
fg_cyan_c    = "\033[36m" # INFO color
fg_grey_c    = "\033[37m"

bg_black_c   = "\033[40m"
bg_red_c     = "\033[41m"
bg_green_c   = "\033[42m"
bg_yellow_c  = "\033[43m"
bg_blue_c    = "\033[44m"
bg_magenta_c = "\033[45m"
bg_cyan_c    = "\033[46m"
bg_grey_c    = "\033[47m"

reset_c      = "\033[0m" # RESET color
bold_c       = "\033[1m"
dim_c        = "\033[2m"
italic_c     = "\033[3m"
underline_c  = "\033[4m"
sblink_c     = "\033[5m"
fblink_c     = "\033[6m"
invert_c     = "\033[7m"
hidden_c     = "\033[8m"
strike_c     = "\033[9m"

# Define Function
def title_p(title_value):
	return "[%s %s %s]\n%s\n" % (fg_cyan_c, title_value, reset_c, ("="*64))

def subtitle_p(subtitle_value):
	return "[%s %s %s]\n%s\n" % (fg_cyan_c, subtitle_value, reset_c, ("-"*64))

def info_p(info_value):
	return "[%s*%s] %s" % (fg_cyan_c, reset_c, info_value)

def success_p(success_value):
	return "[%so%s] %s%s SUCCESS %s %s" % (fg_green_c, reset_c, invert_c, fg_green_c, reset_c, success_value)

def warning_p(warning_value):
	return "[%s!%s] %s%s WARNING %s %s" % (fg_yellow_c, reset_c, invert_c, fg_yellow_c, reset_c, warning_value)

def error_p(error_value):
	return "[%s!%s] %s%s  ERROR  %s %s" % (fg_red_c, reset_c, invert_c, fg_red_c, reset_c, error_value)

def question_p(question_value, answer_value):
	def answer_p(answer_value):
		index = 1
		answer_o = ""

		for answer in answer_value:
			answer_o = answer_o + "[%s%s%s] %s\n" % (fg_cyan_c, index, reset_c, answer)
			index    = index + 1

		return answer_o

	return "[%s?%s] %s\n%s" % (fg_yellow_c, reset_c, question_value, answer_p(answer_value))

def text_p(text_value, width=64):
	return "\n".join(textwrap.wrap(text_value, width=width))

# Main Program
def main():
	answer = ""
	print(title_p("JUDUL PROGRAM"))
	print(subtitle_p("SUB-TITLE PROGRAM"))
	print(info_p("INFO PROGRAM"))
	print(warning_p("WARNING PROGRAM"))
	print(error_p("ERROR PROGRAM"))
	print(success_p("SUCCESS PRORGAM"))
	print(question_p("QUESITON PROGRAM", ["ANSWER 1", "ANSWER 2", "ANSWER 3"]))
	answer = input("> ")
	print(text_p("Kekuatan rakyat untuk masyarakat sejahtera dengan Kekuatan rakyat untuk masyarakat sejahtera dengan Kekuatan rakyat"))

if __name__ == '__main__':
	main()