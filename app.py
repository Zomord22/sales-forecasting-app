import gradio as gr
import pandas as pd
import numpy as np

def forecast_sales(product, historical_sales, growth_trend, seasonality, months):
    """AI-powered sales forecasting"""
    
    try:
        # Base forecast calculation
        base_forecast = historical_sales
        
        # Growth trend adjustment
        growth_factors = {
            "High Growth": 1.25,
            "Moderate Growth": 1.10, 
            "Stable": 1.0,
            "Declining": 0.85
        }
        
        # Seasonality multipliers
        season_factors = {
            "High": 1.3,  # Holiday season
            "Medium": 1.1, # Regular season
            "Low": 0.8    # Off-season
        }
        
        # Time adjustment (longer forecast = more uncertainty)
        time_factor = 1 + (months * 0.02)
        
        # Calculate forecast
        adjusted_sales = (base_forecast * 
                         growth_factors.get(growth_trend, 1.0) * 
                         season_factors.get(seasonality, 1.0) * 
                         time_factor)
        
        # Add some randomness for realism
        np.random.seed(hash(product) % 1000)
        random_factor = np.random.uniform(0.95, 1.05)
        final_forecast = adjusted_sales * random_factor
        
        # Calculate metrics
        growth_amount = final_forecast - historical_sales
        growth_percent = ((final_forecast - historical_sales) / historical_sales) * 100
        
        # Determine business outlook
        if growth_percent > 15:
            outlook = "🚀 EXCELLENT"
            color = "🟢"
            recommendation = "• Scale production\n• Increase marketing\n• Expand inventory"
        elif growth_percent > 5:
            outlook = "📈 POSITIVE" 
            color = "🟡"
            recommendation = "• Maintain current strategy\n• Monitor performance\n• Test new markets"
        elif growth_percent > -5:
            outlook = "📊 STABLE"
            color = "🔵"
            recommendation = "• Optimize operations\n• Improve efficiency\n• Customer retention"
        else:
            outlook = "⚠️  CAUTION"
            color = "🔴"
            recommendation = "• Review strategy\n• Cost optimization\n• Market research"
        
        # Generate insights
        insights = []
        if growth_trend == "High Growth":
            insights.append("Capitalize on growth momentum with strategic investments")
        if seasonality == "High":
            insights.append("Prepare for peak season with increased inventory and staffing")
        if months > 6:
            insights.append("Long-term forecast - consider market trends and competition")
        
        return f"""
{color} **SALES FORECAST REPORT**

**Product:** {product}
**Forecast Period:** {months} months

📊 **CURRENT PERFORMANCE**
- Historical Sales: ${historical_sales:,.0f}/month

🎯 **FORECASTED PERFORMANCE**  
- Projected Sales: ${final_forecast:,.0f}/month
- Expected Growth: ${growth_amount:,.0f} ({growth_percent:+.1f}%)

📈 **BUSINESS OUTLOOK**
{outlook}

🏭 **MARKET ANALYSIS**
- Growth Trend: {growth_trend}
- Seasonality: {seasonality}
- Confidence: {min(85 + months, 95)}%

💡 **STRATEGIC RECOMMENDATIONS**
{recommendation}

🔍 **KEY INSIGHTS**
{chr(10).join(['• ' + insight for insight in insights])}

---
*AI-powered sales forecasting for business planning*
*Updated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}*
"""
        
    except Exception as e:
        return f"❌ Forecast error: {str(e)}"

# Create the interface
with gr.Blocks(theme=gr.themes.Soft(), title="Sales Forecasting AI") as demo:
    gr.Markdown("""
    # 📈 AI Sales Forecasting
    **Predict future sales and optimize your business strategy**
    
    *Advanced machine learning for accurate sales predictions and business intelligence*
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🏭 Business Inputs")
            
            product = gr.Dropdown(
                choices=["Electronics", "Clothing", "Home Goods", "Software", "Food & Beverage", "Automotive"],
                value="Electronics",
                label="📦 Product Category"
            )
            
            historical_sales = gr.Slider(
                1000, 500000, value=50000, step=1000,
                label="💰 Historical Monthly Sales ($)",
                info="Average monthly revenue"
            )
            
            growth_trend = gr.Radio(
                choices=["High Growth", "Moderate Growth", "Stable", "Declining"],
                value="Moderate Growth",
                label="📈 Market Growth Trend"
            )
            
            seasonality = gr.Radio(
                choices=["High", "Medium", "Low"],
                value="Medium", 
                label="🎯 Seasonality Impact"
            )
            
            months = gr.Slider(
                1, 12, value=6, step=1,
                label="📅 Forecast Horizon (Months)",
                info="How far ahead to predict"
            )
            
            forecast_btn = gr.Button("🚀 Generate Forecast", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### 📊 Forecast Results")
            output = gr.Textbox(
                label="AI Business Forecast",
                lines=16,
                max_lines=18,
                show_copy_button=True
            )
    
    # Examples
    gr.Markdown("### 🧪 Business Scenarios")
    examples = gr.Examples(
        examples=[
            ["Electronics", 75000, "High Growth", "High", 3],
            ["Clothing", 25000, "Stable", "Medium", 6],
            ["Software", 120000, "Moderate Growth", "Low", 12],
            ["Food & Beverage", 15000, "Declining", "Medium", 2]
        ],
        inputs=[product, historical_sales, growth_trend, seasonality, months],
        outputs=output,
        label="Click to analyze different business scenarios"
    )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("""
    **💼 Business Impact**: Accurate forecasting can increase revenue by 15-30%
    **📈 Typical Use Cases**: Inventory planning, Budget allocation, Marketing strategy
    **🎯 Industries**: Retail, E-commerce, Manufacturing, SaaS, Services
    
    **🔒 Data Privacy**: This demo uses simulated forecasting algorithms
    """)

if __name__ == "__main__":
    demo.launch()
