import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the data
df = pd.read_csv('Superstore.csv', encoding='latin1')

# Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Dictionary to map full state names to abbreviations
state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Convert full state names to abbreviations
df['State'] = df['State'].map(state_abbreviations)

# Coordinates for states (latitude, longitude)
state_coordinates = {
    'CA': (36.7783, -119.4179),  # California
    'FL': (27.6648, -81.5158),   # Florida
    'NY': (40.7128, -74.0060),   # New York
    # Add more states as needed
}

# Coordinates for cities (latitude, longitude)
city_coordinates = {
    'Los Angeles': (34.0522, -118.2437),
    'San Francisco': (37.7749, -122.4194),
    'Miami': (25.7617, -80.1918),
    'Orlando': (28.5383, -81.3792),
    'New York': (40.7128, -74.0060),
    'Buffalo': (42.8864, -78.8784),
    # Add more cities as needed
}

# Define a color palette for categories
category_colors = {
    'Furniture': '#1f77b4',  # Blue
    'Office Supplies': '#ff7f0e',  # Orange
    'Technology': '#2ca02c'  # Green
}

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Analysis - Superstore Dataset"),
    
    # Dropdown to select a region
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': region, 'value': region} for region in df['Region'].unique()],
        value='All',
        placeholder="Select a region"
    ),
    
    # Graph 1: Sales by Category
    dcc.Graph(id='sales-by-category'),
    
    # Graph 2: Sales Over Time
    dcc.Graph(id='sales-over-time'),
    
    # Graph 3: Sales by State (Map)
    dcc.Graph(id='sales-by-state-map'),
    
    # Graph 4: Sales by Sub-Category (Colored by Category)
    dcc.Graph(id='sales-by-subcategory'),
    
    # Graph 5: Profit by Sub-Category (Colored by Category)
    dcc.Graph(id='profit-by-subcategory'),
    
    # Graph 6: Average Discount by Category
    dcc.Graph(id='discount-by-category'),
    
    # Graph 7: Top 10 Products by Quantity Sold
    dcc.Graph(id='quantity-by-product'),
    
    # Graph 8: Sales and Profit by Customer Segment
    dcc.Graph(id='performance-by-segment'),
    
    # Graph 9: Sales and Profit by Ship Mode
    dcc.Graph(id='performance-by-shipmode'),
    
    # Graph 10: Top 10 Cities by Sales
    dcc.Graph(id='sales-by-city'),
    
    # Graph 11: Monthly Sales Over Time
    dcc.Graph(id='sales-by-month'),
    
    # Graph 12: Top 10 Customers by Profit
    dcc.Graph(id='profit-by-customer')
])

# Define the callback to update the graphs
@app.callback(
    [Output('sales-by-category', 'figure'),
     Output('sales-over-time', 'figure'),
     Output('sales-by-state-map', 'figure'),
     Output('sales-by-subcategory', 'figure'),
     Output('profit-by-subcategory', 'figure'),
     Output('discount-by-category', 'figure'),
     Output('quantity-by-product', 'figure'),
     Output('performance-by-segment', 'figure'),
     Output('performance-by-shipmode', 'figure'),
     Output('sales-by-city', 'figure'),
     Output('sales-by-month', 'figure'),
     Output('profit-by-customer', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('sales-by-state-map', 'clickData')]  # Add clickData as input
)
def update_graphs(selected_region, clickData):
    # Filter the data based on the selected region
    filtered_df = df if selected_region == 'All' else df[df['Region'] == selected_region]
    
    # Graph 1: Sales by Category
    sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    sales_by_category = sales_by_category.sort_values(by='Sales', ascending=False)
    fig1 = px.bar(
        sales_by_category,
        x='Category',
        y='Sales',
        title='Sales by Category',
        color='Category',
        color_discrete_map=category_colors
    )
    
    # Graph 2: Sales Over Time
    sales_over_time = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
    fig2 = px.line(sales_over_time, x='Order Date', y='Sales', title='Sales Over Time')
    
    # Graph 3: Sales by State (Map)
    sales_by_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
    sales_by_state = sales_by_state.sort_values(by='Sales', ascending=True)
    
    # Create the base choropleth map
    fig3 = px.choropleth(
        sales_by_state,
        locations='State',
        locationmode='USA-states',
        color='Sales',
        scope='usa',
        title='Sales by State',
        color_continuous_scale='Viridis'
    )
    
    # Add city-level scatter plot if a state is clicked
    if clickData:
        selected_state = clickData['points'][0]['location']
        
        # Filter data for the selected state
        sales_by_city_for_state = filtered_df[filtered_df['State'] == selected_state].groupby('City')['Sales'].sum().reset_index()
        
        # Add coordinates to the dataframe
        sales_by_city_for_state['Latitude'] = sales_by_city_for_state['City'].map(lambda x: city_coordinates.get(x, (None, None))[0])
        sales_by_city_for_state['Longitude'] = sales_by_city_for_state['City'].map(lambda x: city_coordinates.get(x, (None, None))[1])
        
        # Remove rows with missing coordinates
        sales_by_city_for_state = sales_by_city_for_state.dropna(subset=['Latitude', 'Longitude'])
        
        # Add scatter plot for cities
        fig3.add_trace(
            px.scatter_geo(
                sales_by_city_for_state,
                lat='Latitude',
                lon='Longitude',
                size='Sales',
                color='Sales',
                hover_name='City',
                scope='usa',
                title=f'Sales by City in {selected_state}'
            ).data[0]
        )
        
        # Zoom on the selected state
        state_lat, state_lon = state_coordinates.get(selected_state, (None, None))
        if state_lat and state_lon:
            fig3.update_geos(
                center={"lat": state_lat, "lon": state_lon},
                projection_scale=5  # Adjust zoom level
            )
    
    # Graph 4: Sales by Sub-Category (Colored by Category)
    sales_by_subcategory = filtered_df.groupby(['Sub-Category', 'Category'])['Sales'].sum().reset_index()
    sales_by_subcategory = sales_by_subcategory.sort_values(by='Sales', ascending=False)
    fig4 = px.bar(
        sales_by_subcategory,
        x='Sub-Category',
        y='Sales',
        color='Category',
        title='Sales by Sub-Category (Colored by Category)',
        labels={'Sub-Category': 'Sub-Category', 'Sales': 'Total Sales'},
        color_discrete_map=category_colors
    )
    
    # Graph 5: Profit by Sub-Category (Colored by Category)
    profit_by_subcategory = filtered_df.groupby(['Sub-Category', 'Category'])['Profit'].sum().reset_index()
    profit_by_subcategory = profit_by_subcategory.sort_values(by='Profit', ascending=False)
    fig5 = px.bar(
        profit_by_subcategory,
        x='Sub-Category',
        y='Profit',
        color='Category',
        title='Profit by Sub-Category (Colored by Category)',
        labels={'Sub-Category': 'Sub-Category', 'Profit': 'Total Profit'},
        color_discrete_map=category_colors
    )
    
    # Graph 6: Average Discount by Category
    discount_by_category = filtered_df.groupby('Category')['Discount'].mean().reset_index()
    discount_by_category = discount_by_category.sort_values(by='Discount', ascending=False)
    fig6 = px.bar(
        discount_by_category,
        x='Category',
        y='Discount',
        title='Average Discount by Category',
        labels={'Category': 'Category', 'Discount': 'Average Discount'}
    )
    
    # Graph 7: Top 10 Products by Quantity Sold
    quantity_by_product = filtered_df.groupby('Product Name')['Quantity'].sum().reset_index()
    quantity_by_product = quantity_by_product.sort_values(by='Quantity', ascending=False).head(10)
    fig7 = px.bar(
        quantity_by_product,
        x='Quantity',
        y='Product Name',
        orientation='h',
        title='Top 10 Products by Quantity Sold',
        labels={'Product Name': 'Product', 'Quantity': 'Total Quantity Sold'}
    )
    
    # Graph 8: Sales and Profit by Customer Segment
    performance_by_segment = filtered_df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig8 = px.bar(
        performance_by_segment,
        x='Segment',
        y=['Sales', 'Profit'],
        barmode='group',
        title='Sales and Profit by Customer Segment',
        labels={'Segment': 'Customer Segment', 'value': 'Amount'}
    )
    
    # Graph 9: Sales and Profit by Ship Mode
    performance_by_shipmode = filtered_df.groupby('Ship Mode').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig9 = px.bar(
        performance_by_shipmode,
        x='Ship Mode',
        y=['Sales', 'Profit'],
        barmode='group',
        title='Sales and Profit by Ship Mode',
        labels={'Ship Mode': 'Shipping Mode', 'value': 'Amount'}
    )
    
    # Graph 10: Top 10 Cities by Sales
    sales_by_city = filtered_df.groupby('City')['Sales'].sum().reset_index()
    sales_by_city = sales_by_city.sort_values(by='Sales', ascending=False).head(10)
    fig10 = px.bar(
        sales_by_city,
        x='City',
        y='Sales',
        title='Top 10 Cities by Sales',
        labels={'City': 'City', 'Sales': 'Total Sales'}
    )
    
    # Graph 11: Monthly Sales Over Time
    filtered_df['YearMonth'] = filtered_df['Order Date'].dt.to_period('M').astype(str)
    sales_by_month = filtered_df.groupby('YearMonth')['Sales'].sum().reset_index()
    fig11 = px.line(
        sales_by_month,
        x='YearMonth',
        y='Sales',
        title='Monthly Sales Over Time',
        labels={'YearMonth': 'Month', 'Sales': 'Total Sales'}
    )
    
    # Graph 12: Top 10 Customers by Profit
    profit_by_customer = filtered_df.groupby('Customer Name')['Profit'].sum().reset_index()
    profit_by_customer = profit_by_customer.sort_values(by='Profit', ascending=False).head(10)
    fig12 = px.bar(
        profit_by_customer,
        x='Customer Name',
        y='Profit',
        title='Top 10 Customers by Profit',
        labels={'Customer Name': 'Customer', 'Profit': 'Total Profit'}
    )
    
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)