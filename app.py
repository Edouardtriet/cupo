import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate occupancy details
def calculate_occupancy(avg_check_size, fb_cost_percentage, max_covers, daily_covers):
    fb_cost_percentage /= 100  # Convert to decimal
    total_empty_seats = 0
    total_gross_profit = 0
    missed_profits = []
    
    for covers in daily_covers:
        empty_seats = max_covers - covers
        total_empty_seats += empty_seats
        gross_profit = covers * avg_check_size * (1 - fb_cost_percentage)
        total_gross_profit += gross_profit
        missed_profit = empty_seats * avg_check_size * (1 - fb_cost_percentage)
        missed_profits.append(missed_profit)
    
    total_max_profit = 7 * max_covers * avg_check_size * (1 - fb_cost_percentage)
    total_missed_profit = total_max_profit - total_gross_profit
    overall_occupancy_rate = (sum(daily_covers) / (max_covers * 7)) * 100
    
    return {
        'total_empty_seats': total_empty_seats,
        'total_gross_profit': total_gross_profit,
        'total_missed_profit': total_missed_profit,
        'overall_occupancy_rate': overall_occupancy_rate,
        'missed_profits': missed_profits
    }

# UI Layout
st.title('Restaurant Occupancy Calculator')

st.header('Enter Your Current Occupancy Details')
st.markdown("<br>", unsafe_allow_html=True)  # Adding space

# User Inputs in compact layout
col1, col2, col3 = st.columns(3)
with col1:
    avg_check_size = st.slider('Average Check Size Per Person (€)', 0, 200, 42)
with col2:
    fb_cost_percentage = st.slider('F&B Cost As a % of Sales', 0.0, 100.0, 31.0)
with col3:
    max_covers = st.number_input('Max. covers you could do in a single day', 1, 500, 200)

daily_covers = []
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

col4, col5, col6, col7 = st.columns(4)
with col4:
    daily_covers.append(st.number_input('Total Covers on Monday', 0, max_covers, 50))
    daily_covers.append(st.number_input('Total Covers on Tuesday', 0, max_covers, 60))
with col5:
    daily_covers.append(st.number_input('Total Covers on Wednesday', 0, max_covers, 85))
    daily_covers.append(st.number_input('Total Covers on Thursday', 0, max_covers, 90))
with col6:
    daily_covers.append(st.number_input('Total Covers on Friday', 0, max_covers, 110))
    daily_covers.append(st.number_input('Total Covers on Saturday', 0, max_covers, 165))
with col7:
    daily_covers.append(st.number_input('Total Covers on Sunday', 0, max_covers, 130))

# Calculate Results
results = calculate_occupancy(avg_check_size, fb_cost_percentage, max_covers, daily_covers)

# Display Results
st.header('Your Occupancy Report')

st.subheader('For this given week, here\'s a breakdown of your occupancy...')

st.markdown("<br>", unsafe_allow_html=True)  # Adding space

st.markdown(f'<div style="text-align: center;">You had this many empty seats: <strong>{results["total_empty_seats"]}</strong></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;">You missed out on this much gross profit: <strong>€{results["total_missed_profit"]:.2f}</strong></div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center;">Your overall occupancy rate was: <strong>{results["overall_occupancy_rate"]:.2f}%</strong></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  # Adding space
st.markdown("<br>", unsafe_allow_html=True)  # Adding space

# Display missed profits by day in a bar chart
st.subheader('Missed Gross Profits by Day')
missed_data = pd.DataFrame({
    'Day': days,
    'Missed Gross Profit': results['missed_profits']
})

fig, ax = plt.subplots()
ax.bar(missed_data['Day'], missed_data['Missed Gross Profit'], color='green')

ax.set_ylabel('Missed Gross Profit (€)')
ax.set_xlabel('Day of Week')
ax.set_title('Missed Gross Profits by Day')

# Reduce the size of the day labels
plt.xticks(rotation=45, fontsize=10)

# Adding Euro symbol to Y-axis
import matplotlib.ticker as ticker
formatter = ticker.FormatStrFormatter('€%1.0f')
ax.yaxis.set_major_formatter(formatter)

st.pyplot(fig)

# Display weekday and weekend occupancy scores with specified formatting
def display_occupancy_score(title, occupancy_rate, missed_profit, missed_tips, daily_rates, daily_profits, days):
    st.markdown("<br>", unsafe_allow_html=True)  # Adding space
    st.subheader(title)
    st.markdown(f'<div style="text-align: center;">Occupancy Rate: <strong>{occupancy_rate:.1f}%</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center;">You missed out on <span style="color:red;font-weight:bold;">€{missed_profit:,.2f}</span> in gross profits.</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center;">You\'re losing <span style="color:red;font-weight:bold;">€{missed_tips:,.2f}</span> annually by not filling empty seats.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # Adding space
    cols = st.columns(len(days))
    for i, day in enumerate(days):
        rate_color = 'green' if daily_rates[i] > 80 else 'red'
        profit_color = 'red'
        with cols[i]:
            st.markdown(f'**{day}**')
            st.markdown(f'Occupancy Rate: **<span style="color:{rate_color};">{daily_rates[i]:.1f}%</span>**', unsafe_allow_html=True)
            st.markdown(f'Missed Profit: **<span style="color:{profit_color};">€{daily_profits[i]:,.2f}</span>**', unsafe_allow_html=True)

weekday_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekend_days = ['Saturday', 'Sunday']

weekday_rates = [daily_covers[i] / max_covers * 100 for i in range(5)]
weekend_rates = [daily_covers[i] / max_covers * 100 for i in range(5, 7)]
weekday_profits = results['missed_profits'][:5]
weekend_profits = results['missed_profits'][5:]

display_occupancy_score('Weekday Occupancy Score', 
                        sum(weekday_rates) / 5, 
                        sum(weekday_profits), 
                        sum(weekday_profits) * 52, 
                        weekday_rates, 
                        weekday_profits,
                        weekday_days)

display_occupancy_score('Weekend Occupancy Score', 
                        sum(weekend_rates) / 2, 
                        sum(weekend_profits), 
                        sum(weekend_profits) * 52, 
                        weekend_rates, 
                        weekend_profits,
                        weekend_days)

# Display occupancy action plan
st.subheader('Occupancy Action Plan')
gross_margin = (100 - fb_cost_percentage)  # Gross margin percentage
contribution_per_cover = avg_check_size * (gross_margin)/100
st.markdown(f'<div style="text-align: center;">Each empty seat filled has a gross margin of <span style="color:green;font-weight:bold;">{gross_margin:.1f}%</span> and contributes <span style="color:green;font-weight:bold;">€{contribution_per_cover:.2f}</span> to your gross profit.</div>', unsafe_allow_html=True)

potential_increase = (results['total_empty_seats'] * 0.2) * contribution_per_cover
annual_increase = potential_increase * 52  # Assuming 52 weeks in a year

st.markdown('<div style="background-color:#e8f5e9;padding:10px;">'
            f'If you are able to fill just 20% of your {results["total_empty_seats"]} empty seats each week, you will...'
            '</div>', unsafe_allow_html=True)
st.markdown('<div style="background-color:#e8f5e9;padding:10px;text-align: center;">'
            f'<span style="color:green;font-weight:bold;">Increase profit margins annually by €{annual_increase:.2f}</span>'
            '</div>', unsafe_allow_html=True)


