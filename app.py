import streamlit as st

import math

from matplotlib import pyplot as plt

import pandas as pd

import random

st.set_page_config(
    page_title="Shark Tank Simulator",
    page_icon="🦈",
    layout="wide"
)

st.title("Shark Tank Simulator V2")
st.divider()

if "page" not in st.session_state:
    st.session_state.page="home"
    st.session_state.current_page="Home"

if "data" not in st.session_state:
    st.session_state.data=[]

if "names" not in st.session_state:
    st.session_state.names=[]

if "total" not in st.session_state:
    st.session_state.total=0

st.sidebar.title(f"Total Net Return:")
if st.session_state.total<0:
    st.sidebar.error(f"-${st.session_state.total*-1:,.2f}")
if st.session_state.total>0:
    st.sidebar.success(f"${st.session_state.total:,.2f}")
if st.session_state.total==0:
    st.sidebar.write(f"${st.session_state.total:,.2f}")
st.sidebar.divider()
st.sidebar.title("Game Progress")
stages = ["Home",
          "Choose Difficulty",
          "Business Basics",
          "Performance",
          "Deal Terms",
          "Decision",
          "Result",
          "Analysis",
          "Post-Game Analysis"]

for stage in stages:
    if stage == st.session_state.current_page:
        st.sidebar.write(f"➤ **{stage}**")
    else:
        st.sidebar.write(stage)

class Entrepreneur:
    def __init__(self, name):
        self.name = name
        self.product_price=0
        if self.name == "Hunter":
            self.product_price = random.randint(25, 50)
            self.manufacturing_cost = random.randint(16, 19)
            self.products_sold = random.randint(5, 20) * 1000
        elif self.name == "Annie":
            self.product_price = random.randint(10, 25) * 100
            self.manufacturing_cost = random.randint(self.product_price-350, self.product_price-150)
            self.products_sold = random.randint(10, 25) * 100
        elif self.name == "Oliver":
            self.product_price = random.randint(10, 20) * 10
            self.manufacturing_cost = random.randint(7, 9) * 10
            self.products_sold = random.randint(5, 25) * 100
        self.profit_margin = (self.product_price-self.manufacturing_cost)/self.product_price
        self.profit = (self.product_price-self.manufacturing_cost)*self.products_sold
        self.predicted_increase=random.randint(20, 40)/100
        self.max_equity = random.randint(10, 25)
        self.asking_equity = random.randint(1, self.max_equity)
        self.asking_price = random.randint(1, 6)*50000
        self.equity=0

    def offer(self, equity):
       if equity<=self.max_equity:
           self.equity=equity
           return True
       return False

    def result(self):
        company_profit=[]
        company_profit_formatted=[]
        percentages=[]
        sum=0
        for i in range(5):
            increase = random.uniform(self.predicted_increase-0.1, self.predicted_increase+0.1)
            percentages.append(f"{increase*100:,.1f}%")
            if i==0:
                year_profit = (self.product_price-self.manufacturing_cost)*self.products_sold*(1+increase)
                company_profit_formatted.append(f"{year_profit:,.2f}")
                company_profit.append(year_profit)
                sum+=year_profit*(self.equity/100)
            else:
                year_profit = company_profit[i-1]*(1+increase)
                company_profit_formatted.append(f"{year_profit:,.2f}")
                company_profit.append(year_profit)
                sum+=year_profit*(self.equity/100)
        table={"Growth(%)":percentages, "Company Profit":company_profit_formatted}
        df=pd.DataFrame(table)
        df.index=[1,2,3,4,5]
        df.index.name="Year"
        st.dataframe(df, width="stretch")
        st.session_state.data.append(company_profit)
        if self.name not in st.session_state.names:
            st.session_state.names.append(self.name)
        plt.plot([1,2,3,4,5], company_profit, color="g")
        plt.title("Company Profit Over 5 Years")
        plt.xlabel("Years")
        plt.ylabel("Company Profit($)")
        plt.xticks([1,2,3,4,5])
        plt.ticklabel_format(style="plain", axis="y")
        st.pyplot(plt)
        plt.close()

        return sum-self.asking_price

if "answers" not in st.session_state:
    st.session_state.answers=["", "", "", "", "", "", "", ""]

if "name" not in st.session_state:
    st.session_state.name=""

def game(name, idea):
    st.session_state.name=name
    st.header(name)
    st.caption(idea)
    if q_and_a(0, f"**Product Price: ${st.session_state.entrepreneur.product_price:,.2f}**", name):
        if q_and_a(1,f"**Cost of Manufacturing: ${st.session_state.entrepreneur.manufacturing_cost:,.2f}**", name):
            if q_and_a(2,f"**Profit Margin: {st.session_state.entrepreneur.profit_margin*100:.1f}%**", name):
                if q_and_a(3,f"**Products Sold: {st.session_state.entrepreneur.products_sold:,}**", name):
                    st.session_state.page="Performance"
                    st.session_state.current_page="Performance"
                    st.rerun()

def q_and_a(num, question,name):
    if question == "increase":
        list=[]
        for i in range(5):
            list.append(100*random.uniform(st.session_state.entrepreneur.predicted_increase-0.12, st.session_state.entrepreneur.predicted_increase-0.02))
        plt.plot([1,2,3,4,5], list, color="red")
        plt.title("Growth(%)")
        plt.xlabel("Years")
        plt.ylabel("Company Growth Rate")
        plt.xticks([1,2,3,4,5])
        st.pyplot(plt)
        plt.close()
    else:
        st.write(question)
    st.session_state.answers[num]=st.radio("Your Assessment:", ["Strong", "Neutral", "Concern"], index=None, key=f"{name}_answer{num}")
    if st.session_state.answers[num]=="Strong" or st.session_state.answers[num]=="Neutral" or st.session_state.answers[num]=="Concern":
        return True

if st.session_state.page=="Performance":

    if q_and_a(4,f"**Profit(Last Year): ${st.session_state.entrepreneur.profit:,.2f}**",st.session_state.name):
        if q_and_a(5,"increase",st.session_state.name):
            st.session_state.page="Deal Terms"
            st.session_state.current_page="Deal Terms"
            st.rerun()

if st.session_state.page=="Deal Terms":
    if q_and_a(6,f"**{st.session_state.name} is asking for ${st.session_state.entrepreneur.asking_price:,.2f}**",st.session_state.name):
        if q_and_a(7, f"**{st.session_state.entrepreneur.asking_equity}% of their business**", st.session_state.name):
            st.session_state.page="table"
            st.session_state.current_page="Decision"
            st.rerun()

def instructions():
    return st.write("""
Welcome to Shark Tank Simulator

In this game you will be playing as an investor with infinite money.

There are three levels of difficulty: easy, medium, and hard.

Depending on what level you choose, you will be given an entrepreneur with an idea.

If you choose easy, it will be easy to make a profit from your investment, and if you choose hard, it will be hard to make a profit, and so on.
However, it is not impossible to make a profit or loss for any level.

Format

Each entrepreneur will give you their:
- Name
- Idea
- Product price
- Manufacturing price
- Profit margin
- Number of products sold
- Profit from sales
- Percent increase in sales per year
- Their deal, including how much money they are asking for in exchange for a certain percentage of equity.

Important Vocabulary

Expenses - Things that you need to pay for in order to make a profit. More is bad.

Profit - The money you make after subtracting all expenses. More is good.

Product Price - The price a customer pays to buy the product. More is good.

Cost of Manufacturing - The amount of money required to produce the product. More is bad.

Profit Margin - The percentage of money you keep after subtracting expenses. A higher profit margin is generally good, but it does not necessarily mean higher profit.

    Example 1:
    Product sells for $2 and earns a $1 profit.
    Profit Margin = 50%

    Example 2:
    Product sells for $100 and earns a $20 profit.
    Profit Margin = 20%

    Even though the first product has a higher profit margin, the second product earns much more profit.

Products Sold - The number of products sold by the business. More is good.

Percent Increase - The yearly percentage increase in products sold. More is good.

Equity - The percentage of the company you own. More is good. You can negotiate for more equity during a deal.

ROI (Return on Investment) - Measures how much money you made or lost from an investment. More is good.

Try to make the most money possible by making smart investments!
""")

if "difficulties" not in st.session_state:
    st.session_state.difficulties=[False, False, False]

if "slider" not in st.session_state:
    st.session_state.slider=False

if st.session_state.page=="home":
    st.write("""
             
     Analyze businesses. Make deals. Test your decisions.

    You are the Shark.

    Evaluate entrepreneurs using their financial data, determine
    whether their businesses are worth investing in, and negotiate
    for equity when you think you can get a better deal.

    Your decisions will be tested over a five-year simulation.
""")
    if st.button("Play▶️"):
        st.session_state.page="difficulty"
        st.session_state.current_page="Choose Difficulty"
        st.rerun()
    with st.expander("How to Play"):
        instructions()
    st.markdown("""
<style>
.info-button {
    position: fixed;
    bottom: 25px;
    right: 25px;

    width: 50px;
    height: 50px;
    border-radius: 50%;

    background-color: #0068c9;
    color: white !important;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 24px;
    text-decoration: none !important;
}

.info-button:hover {
    background-color: #0054a3;
}
</style>

<a class="info-button"
   href="https://github.com/28krishiv-gif/Shark-Tank-Simulator-V2/blob/main/README.md"
   target="_blank">
    ⓘ
</a>
""", unsafe_allow_html=True)
elif st.session_state.page=="difficulty":
    st.session_state.is_added=False
    if not st.session_state.difficulties[0] or not st.session_state.difficulties[1] or not st.session_state.difficulties[2]:
        st.header("Choose Your Difficulty")
        st.caption("Select how challenging you want the investment analysis to be.")
        easy, medium, hard = st.columns(3)

    if not st.session_state.difficulties[0]:
        with easy:    
            st.subheader("Easy")
            st.write("Clearer financial signals and more straightforward decisions.")
            if st.button("Choose Easy", width="stretch"):
                st.session_state.difficulties[0] = True
                st.session_state.entrepreneur = Entrepreneur("Annie")
                st.session_state.page="easy"
                st.session_state.current_page="Business Basics"
                st.rerun()
    if not st.session_state.difficulties[1]:
        with medium:
            st.subheader("Medium")
            st.write("Mixed financial signals that require more careful analysis.")
            if st.button("Choose Medium", width="stretch"):
                st.session_state.difficulties[1] = True
                st.session_state.entrepreneur = Entrepreneur("Hunter")
                st.session_state.page="medium"
                st.session_state.current_page="Business Basics"
                st.rerun()
    if not st.session_state.difficulties[2]:
        with hard:
            st.subheader("Hard")
            st.write("Ambiguous businesses where strengths may hide important risks.")
            if st.button("Choose Hard", width="stretch"):
                st.session_state.difficulties[2] = True
                st.session_state.entrepreneur = Entrepreneur("Oliver")
                st.session_state.page="hard"
                st.session_state.current_page="Business Basics"
                st.rerun()
    if st.session_state.difficulties[0] and st.session_state.difficulties[1] and st.session_state.difficulties[2]:
        plt.figure()
        st.header("Investment Results")

        st.metric(
        "Total Net Return",
        f"${st.session_state.total:,.2f}"
        )
        st.subheader("Company Performance")

        for i in range(3):
            if st.session_state.names[i]=="Annie":
                clr = "g"
            elif st.session_state.names[i]=="Hunter":
                clr = "b"
            elif st.session_state.names[i]=="Oliver":
                clr = "r"
            plt.plot([1,2,3,4,5], st.session_state.data[i], color=clr, label=st.session_state.names[i])
            plt.title("Company Profit Over 5 Years")
            plt.xlabel("Years")
            plt.ylabel("Company Profit($)")
            plt.xticks([1,2,3,4,5])
            plt.ticklabel_format(style="plain", axis="y")
        plt.legend()
        st.pyplot(plt)
        if st.button("Play Again"):
            st.session_state.clear()
            st.rerun()
elif st.session_state.page=="easy":
    game("Annie", "A lawn mower that mows the lawn once you tell it to. All by itself.")
elif st.session_state.page=="medium":
    game("Hunter", "A phone case that always protects the phone")
elif st.session_state.page=="hard":
    game("Oliver", "A charger that charges devices using bluetooth.")
elif st.session_state.page=="table":

    st.session_state.questions = [f"Product Price: ${st.session_state.entrepreneur.product_price:,.2f}",
                 f"Cost of Manufacturing: ${st.session_state.entrepreneur.manufacturing_cost:,.2f}",
                 f"Profit Margin: {st.session_state.entrepreneur.profit_margin*100:,.1f}%",
                 f"Products Sold: {st.session_state.entrepreneur.products_sold:,}",
                 f"Profit(Last Year): ${st.session_state.entrepreneur.profit:,.2f}",
                 f"Historical Growth Graph",
                 f"Entrepreneur asked for ${st.session_state.entrepreneur.asking_price:,.2f}",
                 f"Entrepreneur is offering {st.session_state.entrepreneur.asking_equity}% of their business"]

    table={"Information": st.session_state.questions, "Your Assessment": st.session_state.answers}
    df = pd.DataFrame(table)
    st.dataframe(df, width="stretch")

    st.write("Would You like to invest?")
    col1, col2=st.columns(2)

    with col1:
        if st.button("Invest", width="stretch"):
            st.session_state.page="yes"
            st.rerun()
    with col2:
        if st.button("Pass", width="stretch"):
            st.session_state.page="no"
            st.session_state.current_page="Result"
            st.rerun()
elif st.session_state.page=="yes":
    st.header("Finalize Your Investment")
    col1, col2, col3 = st.columns(3)
    col1=st.metric("Asking Price", f"${st.session_state.entrepreneur.asking_price:,.2f}")
    col2=st.metric("Equity Offered", f"{st.session_state.entrepreneur.asking_equity}%")
    col3=st.metric("Last-Year Profit", f"${st.session_state.entrepreneur.profit:,.2f}")
    st.caption("Accept the original deal or negotiate for a larger share of the company.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Accept Deal", use_container_width=True):
            st.session_state.page = "accept"
            st.session_state.current_page = "Result"
            st.rerun()

    with col2:
        if st.button("Negotiate", use_container_width=True):
            st.session_state.page = "negotiate"
            st.rerun()
elif st.session_state.page=="accept":
    st.session_state.entrepreneur.offer(st.session_state.entrepreneur.asking_equity)
    st.write(f"{st.session_state.entrepreneur.name} agrees to your offer.")
    result = st.session_state.entrepreneur.result()
    if result>0:
        st.metric("Total Net Return", f"${result:,.2f}")
    else :
        st.metric("Total Net Return", f"-${-1*result:,.2f}")
    if not st.session_state.is_added:
        st.session_state.total += result
        st.session_state.is_added=True
    if st.button("Continue"):
        st.session_state.page="analysis"
        st.session_state.current_page="Analysis"
        st.rerun()
elif st.session_state.page=="no":
    st.session_state.entrepreneur.offer(st.session_state.entrepreneur.asking_equity)
    result = st.session_state.entrepreneur.result()
    if result>0:
        st.write(f"It seems you missed out on a good deal you could have had a profit of ${result:,.2f}")
    else:
        num = -1*result
        st.write(f"Good decision. If you had taken the deal you have had a loss of ${num:,.2f}")
    if st.button("Continue"):
        st.session_state.page="analysis"
        st.session_state.current_page="Analysis"
        st.rerun()
elif st.session_state.page=="negotiate":
    if not st.session_state.slider:
        st.session_state.equity = st.slider("Select equity amount:", min_value=st.session_state.entrepreneur.asking_equity+1, max_value=100)
    if st.button("Submit Offer"):
        st.session_state.page="result_negotiate"
        st.session_state.current_page="Result"
        st.rerun()
elif st.session_state.page=="result_negotiate":
    offer = st.session_state.entrepreneur.offer(st.session_state.equity)
    if offer:    
        st.write(f"{st.session_state.entrepreneur.name} agrees to your deal")
        result = st.session_state.entrepreneur.result()
        if result>0:
            st.metric("Total Net Return", f"${result:,.2f}")
        else :
            st.metric("Total Net Return", f"-${-1*result:,.2f}")
        if not st.session_state.is_added:
            st.session_state.total += result
            st.session_state.is_added=True
        if st.button("Continue"):
            st.session_state.page="analysis"
            st.session_state.current_page="Analysis"
            st.rerun()
    else:
        st.session_state.entrepreneur.offer(st.session_state.entrepreneur.asking_equity)
        st.write(f"{st.session_state.entrepreneur.name} does not agree to your deal and leaves")
        result = st.session_state.entrepreneur.result()
        if result>0:
            st.write(f"It seems you missed out on a good deal you could have had a profit of ${result:,.2f}")
        else:
            num = -1*result
            st.write(f"Good decision. If you had taken the deal you have had a loss of ${num:,.2f}")
        if st.button("Continue"):
            st.session_state.page="analysis"
            st.session_state.current_page="Analysis"
            st.rerun()
elif st.session_state.page=="analysis":
    game_answers=["","","","","","","",""]
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.product_price<33:
        game_answers[0]="Concern"
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.product_price>=33 and st.session_state.entrepreneur.product_price<=42:
        game_answers[0]="Neutral"
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.product_price>42:
        game_answers[0]="Strong"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.product_price<1500:
        game_answers[0]="Concern"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.product_price>=1500 and st.session_state.entrepreneur.product_price<=2000:
        game_answers[0]="Neutral"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.product_price>2000:
        game_answers[0]="Strong"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.product_price<130:
        game_answers[0]="Concern"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.product_price>=130 and st.session_state.entrepreneur.product_price<=170:
        game_answers[0]="Neutral"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.product_price>170:
        game_answers[0]="Strong"

    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.manufacturing_cost==16:
        game_answers[1]="Strong"
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.manufacturing_cost>16 and st.session_state.entrepreneur.manufacturing_cost<=19:
        game_answers[1]="Neutral"
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.manufacturing_cost==19:
        game_answers[1]="Concern"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.manufacturing_cost<st.session_state.entrepreneur.product_price-284:
        game_answers[1]="Strong"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.manufacturing_cost>=st.session_state.entrepreneur.product_price-284 and st.session_state.entrepreneur.manufacturing_cost<=st.session_state.entrepreneur.product_price-216:
        game_answers[1]="Neutral"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.manufacturing_cost>st.session_state.entrepreneur.product_price-216:
        game_answers[1]="Concern"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.manufacturing_cost==70:
        game_answers[1]="Strong"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.manufacturing_cost==80:
        game_answers[1]="Neutral"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.manufacturing_cost==90:
        game_answers[1]="Concern"
    
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.products_sold<10000:
        game_answers[3]="Concern"
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.products_sold>=10000 and st.session_state.entrepreneur.products_sold<=15000:
        game_answers[3]="Neutral"
    if st.session_state.name=="Hunter" and st.session_state.entrepreneur.products_sold>15000:
        game_answers[3]="Strong"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.products_sold<15000:
        game_answers[3]="Concern"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.products_sold>=15000 and st.session_state.entrepreneur.products_sold<=20000:
        game_answers[3]="Neutral"
    if st.session_state.name=="Annie" and st.session_state.entrepreneur.products_sold>20000:
        game_answers[3]="Strong"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.products_sold<1100:
        game_answers[3]="Concern"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.products_sold>=1100 and st.session_state.entrepreneur.products_sold<=1900:
        game_answers[3]="Neutral"
    if st.session_state.name=="Oliver" and st.session_state.entrepreneur.products_sold>1900:
        game_answers[3]="Strong"
    
    if st.session_state.entrepreneur.profit_margin<0.33:
        game_answers[2]="Concern"
    if st.session_state.entrepreneur.profit_margin>=0.33 and st.session_state.entrepreneur.profit_margin<=0.67:
        game_answers[2]="Neutral"
    if st.session_state.entrepreneur.profit_margin>0.67:
        game_answers[2]="Strong"
    
    if st.session_state.entrepreneur.profit<100000:
        game_answers[4]="Concern"
    if st.session_state.entrepreneur.profit>=100000 and st.session_state.entrepreneur.profit<=300000:
        game_answers[4]="Neutral"
    if st.session_state.entrepreneur.profit>300000:
        game_answers[4]="Strong"
    
    if st.session_state.entrepreneur.predicted_increase<0.26:
        game_answers[5]="Concern"
    if st.session_state.entrepreneur.predicted_increase>=0.26 and st.session_state.entrepreneur.predicted_increase<=0.34:
        game_answers[5]="Neutral"
    if st.session_state.entrepreneur.predicted_increase>0.34:
        game_answers[5]="Strong"
    
    if st.session_state.entrepreneur.equity<math.floor(st.session_state.entrepreneur.max_equity/3):
        game_answers[7]="Concern"
    if st.session_state.entrepreneur.equity>=math.floor(st.session_state.entrepreneur.max_equity/3) and st.session_state.entrepreneur.equity<=math.floor(st.session_state.entrepreneur.max_equity*(2/3)):
        game_answers[7]="Neutral"
    if st.session_state.entrepreneur.equity>math.floor(st.session_state.entrepreneur.max_equity*(2/3)):
        game_answers[7]="Strong"

    if st.session_state.entrepreneur.asking_price==300000 or st.session_state.entrepreneur.asking_price==250000:
        game_answers[6]="Concern"
    if st.session_state.entrepreneur.asking_price==150000 or st.session_state.entrepreneur.asking_price==200000:
        game_answers[6]="Neutral"
    if st.session_state.entrepreneur.asking_price==50000 or st.session_state.entrepreneur.asking_price==100000:
        game_answers[6]="Strong"

    df=pd.DataFrame({"Information": st.session_state.questions, "Response": st.session_state.answers, "Game Assessment": game_answers})
    st.dataframe(df, width="stretch")

    if st.button("Continue"):
        st.session_state.page="difficulty"
        st.session_state.current_page="Choose Difficulty"
        st.rerun()