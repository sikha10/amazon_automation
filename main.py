from amazon.amazon import Amazon
import time

with Amazon() as bot:
    bot.first_page()
    bot.search_product(input("what product do you want: "))
    bot.filter_high_to_low()
    bot.refresh()
    # bot.brand_filter()
    # time.sleep(5)
    try:
        bot.choose_brand(input("choose brand, if you don't want specific brand write 'pass': "))
    except:
        pass
    bot.print_last_page()
    bot.go_to_page(int(input('How many pages of information do you want: ')))

