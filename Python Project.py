import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class AirWiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌫️ AirWise - Air Quality Intelligence App")
        self.root.geometry("1400x800")
        self.root.iconbitmap() if os.name == 'nt' else None  # Add icon in future
        
        # App colors
        self.colors = {
            "superhero": {
                "primary": "#3498db",
                "secondary": "#2c3e50",
                "success": "#00bc8c", 
                "info": "#3498db",
                "warning": "#f39c12",
                "danger": "#e74c3c"
            },
            "flatly": {
                "primary": "#2c3e50",
                "secondary": "#95a5a6",
                "success": "#18bc9c",
                "info": "#3498db", 
                "warning": "#f39c12",
                "danger": "#e74c3c"
            }
        }
        
        self.current_theme = "superhero"
        self.data = None
        self.build_ui()

    def build_ui(self):
        # Main layout
        main_frame = tb.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Banner with gradient
        banner_frame = tb.Frame(main_frame, bootstyle="primary")
        banner_frame.pack(fill="x", pady=(0, 10))
        banner_label = tb.Label(banner_frame, 
                              text="AirWise - Air Quality Intelligence",
                              font=("Helvetica", 18, "bold"),
                              foreground="white", 
                              padding=10)
        banner_label.pack(fill="x")
        
        # Tab control with custom styling
        tab_control = tb.Notebook(main_frame)
        self.tabs = {}

        # Create styled tabs
        for name, icon in [('Data', '📊'), ('EDA', '📈'), ('Visualization', '🔍'), 
                          ('AQI Calc', '🧮'), ('Settings', '⚙️')]:
            frame = tb.Frame(tab_control, padding=15)
            tab_control.add(frame, text=f"{icon} {name}")
            self.tabs[name] = frame

        tab_control.pack(expand=1, fill="both")

        # Data Tab
        data_top_frame = tb.Frame(self.tabs['Data'])
        data_top_frame.pack(fill="x", pady=10)
        
        load_btn = tb.Button(data_top_frame, text="📂 Load Dataset", 
                          command=self.load_data, 
                          bootstyle="primary", 
                          width=15)
        load_btn.pack(side="left", padx=5)
        ToolTip(load_btn, "Load a CSV or Excel dataset for analysis")
        
        # Data display with styling
        self.data_msg = tk.Text(self.tabs['Data'], height=25, bd=0)
        self.data_msg.pack(fill="both", expand=True, pady=5)
        data_scroll = tb.Scrollbar(self.tabs['Data'], command=self.data_msg.yview)
        data_scroll.pack(side="right", fill="y")
        self.data_msg.configure(yscrollcommand=data_scroll.set)

        # EDA Tab
        eda_top_frame = tb.Frame(self.tabs['EDA'])
        eda_top_frame.pack(fill="x", pady=10)
        
        run_eda_btn = tb.Button(eda_top_frame, text="🔍 Run EDA", 
                             command=self.run_eda, 
                             bootstyle="success", 
                             width=15)
        run_eda_btn.pack(side="left", padx=5)
        ToolTip(run_eda_btn, "Perform Exploratory Data Analysis")
        
        # Create a frame for the EDA output with tabs
        eda_output_frame = tb.Frame(self.tabs['EDA'])
        eda_output_frame.pack(fill="both", expand=True, pady=5)
        
        eda_tabs = tb.Notebook(eda_output_frame)
        
        # EDA text output tab
        eda_text_frame = tb.Frame(eda_tabs)
        eda_tabs.add(eda_text_frame, text="Statistics")
        
        self.eda_msg = tk.Text(eda_text_frame, height=15, bd=0)
        self.eda_msg.pack(fill="both", expand=True)
        eda_scroll = tb.Scrollbar(eda_text_frame, command=self.eda_msg.yview)
        eda_scroll.pack(side="right", fill="y")
        self.eda_msg.configure(yscrollcommand=eda_scroll.set)
        
        # EDA plot tab
        self.eda_plot_frame = tb.Frame(eda_tabs)
        eda_tabs.add(self.eda_plot_frame, text="Correlation Plot")
        
        eda_tabs.pack(fill="both", expand=True)

        # Visualization Tab
        viz_top_frame = tb.Frame(self.tabs['Visualization'])
        viz_top_frame.pack(fill="x", pady=10)
        
        viz_btn = tb.Button(viz_top_frame, text="📊 Visualize Data", 
                         command=self.visualize_data, 
                         bootstyle="info", 
                         width=15)
        viz_btn.pack(side="left", padx=5)
        ToolTip(viz_btn, "Generate visualizations from your data")
        
        # Create plot type selection
        self.plot_type = tk.StringVar(value="default")
        plot_select_frame = tb.LabelFrame(viz_top_frame, text="Plot Type", bootstyle="default")
        plot_select_frame.pack(side="left", padx=20)
        
        for plot_type, text in [("default", "Multi-plot"), ("heatmap", "Heatmap"), 
                               ("boxplot", "Boxplots"), ("histogram", "Histograms")]:
            tb.Radiobutton(plot_select_frame, text=text, variable=self.plot_type, 
                         value=plot_type).pack(side="left", padx=10)
        
        # Visualization plot frame
        self.viz_plot_frame = tb.Frame(self.tabs['Visualization'])
        self.viz_plot_frame.pack(fill="both", expand=True, pady=10)

        # AQI Calculator Tab
        aqi_frame = tb.Frame(self.tabs['AQI Calc'])
        aqi_frame.pack(pady=30, fill="both", expand=True)
        
        aqi_left_frame = tb.Frame(aqi_frame)
        aqi_left_frame.pack(side="left", padx=20, fill="both", expand=True)
        
        aqi_input_frame = tb.LabelFrame(aqi_left_frame, text="Calculate Air Quality Index", 
                                     padding=20, bootstyle="info")
        aqi_input_frame.pack(pady=20, fill="x")
        
        tb.Label(aqi_input_frame, text="Enter PM2.5 value (μg/m³):", 
              font=("Helvetica", 12)).pack(pady=(0, 10))
        
        self.pm_entry = tb.Entry(aqi_input_frame, width=15, font=("Helvetica", 12))
        self.pm_entry.pack(pady=10)
        
        calc_btn = tb.Button(aqi_input_frame, text="🧮 Calculate AQI", 
                          command=self.calculate_aqi, 
                          bootstyle="success", 
                          width=15)
        calc_btn.pack(pady=10)
        
        # AQI result display
        self.aqi_result = tk.StringVar()
        result_frame = tb.LabelFrame(aqi_left_frame, text="Results", padding=20)
        result_frame.pack(pady=20, fill="x")
        
        self.aqi_value_label = tb.Label(result_frame, 
                                     textvariable=self.aqi_result, 
                                     font=('Helvetica', 16, 'bold'))
        self.aqi_value_label.pack(pady=10)
        
        self.aqi_desc = tk.StringVar()
        tb.Label(result_frame, textvariable=self.aqi_desc, 
              font=('Helvetica', 12)).pack(pady=5)
        
        # AQI right side - info
        aqi_right_frame = tb.Frame(aqi_frame)
        aqi_right_frame.pack(side="right", padx=20, fill="both", expand=True)
        
        aqi_info_frame = tb.LabelFrame(aqi_right_frame, text="AQI Scale Reference", 
                                     padding=10)
        aqi_info_frame.pack(pady=20, fill="both", expand=True)
        
        # AQI color scale
        aqi_scales = [
            ("Good (0-50)", "Low health risk", "#00e400"),
            ("Moderate (51-100)", "Moderate health risk", "#ffff00"),
            ("Unhealthy for Sensitive Groups (101-150)", "Children and elderly at risk", "#ff7e00"),
            ("Unhealthy (151-200)", "Health effects for everyone", "#ff0000"),
            ("Very Unhealthy (201-300)", "Health alert", "#99004c"),
            ("Hazardous (301+)", "Emergency conditions", "#7e0023")
        ]
        
        for i, (level, desc, color) in enumerate(aqi_scales):
            scale_frame = tb.Frame(aqi_info_frame, bootstyle="default")
            scale_frame.pack(fill="x", pady=5)
            
            color_box = tb.Label(scale_frame, text="   ", background=color, 
                              width=3, borderwidth=1, relief="solid")
            color_box.pack(side="left", padx=5)
            
            level_label = tb.Label(scale_frame, text=level, width=30, 
                                anchor="w", font=("Helvetica", 10, "bold"))
            level_label.pack(side="left", padx=5)
            
            desc_label = tb.Label(scale_frame, text=desc, width=20, anchor="w")
            desc_label.pack(side="left", padx=5)

        # Settings Tab
        settings_frame = tb.Frame(self.tabs['Settings'])
        settings_frame.pack(pady=30, fill="both", expand=True)
        
        appearance_frame = tb.LabelFrame(settings_frame, text="Appearance Settings", 
                                      padding=20, bootstyle="default")
        appearance_frame.pack(pady=20, fill="x")
        
        theme_frame = tb.Frame(appearance_frame)
        theme_frame.pack(fill="x", pady=10)
        
        tb.Label(theme_frame, text="Theme:", 
              font=("Helvetica", 12)).pack(side="left", padx=10)
        
        theme_btn = tb.Button(theme_frame, text="🌗 Toggle Dark/Light Theme", 
                          command=self.toggle_theme, 
                          bootstyle="outline-secondary",
                          width=25)
        theme_btn.pack(side="left", padx=10)
        
        info_frame = tb.LabelFrame(settings_frame, text="About AirWise", 
                                padding=20, bootstyle="default")
        info_frame.pack(pady=20, fill="x")
        
        tb.Label(info_frame, text="AirWise - Air Quality Intelligence App", 
              font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tb.Label(info_frame, text="Version 1.1.0").pack(anchor="w")
        tb.Label(info_frame, text="An application for air quality data analysis and visualization.").pack(anchor="w", pady=5)

        # Status Bar
        status_frame = tb.Frame(self.root)
        status_frame.pack(fill="x", side="bottom")
        
        self.progress = tb.Progressbar(status_frame, mode='determinate', maximum=100)
        self.progress.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.status = tk.StringVar(value="Ready")
        status_label = tb.Label(status_frame, textvariable=self.status, anchor='w')
        status_label.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=2)
        
        # Apply initial theme
        self.update_theme_elements()

    def toggle_theme(self):
        self.current_theme = "flatly" if self.current_theme == "superhero" else "superhero"
        self.root.style.theme_use(self.current_theme)
        self.update_theme_elements()

    def update_theme_elements(self):
        # Update UI elements based on theme
        if hasattr(self, 'aqi_value_label'):
            self.aqi_value_label.configure(foreground=self.colors[self.current_theme]["primary"])

    def set_status(self, text):
        self.status.set(f"🔄 {text}")
        self.progress.start(10)
        self.root.update()

    def complete_status(self, text="Complete"):
        self.status.set(f"✅ {text}")
        self.progress.stop()
        self.progress.config(value=100)
        self.root.update()
        self.root.after(1000, lambda: self.progress.config(value=0))

    def load_data(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx *.xls")])
        if not path:
            return
            
        self.set_status("Loading data...")
        
        try:
            self.data = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
            self.data_msg.delete('1.0', tk.END)
            
            # Styled header
            self.data_msg.insert(tk.END, f"✅ Loaded: {os.path.basename(path)}\n", "header")
            self.data_msg.insert(tk.END, f"Total rows: {self.data.shape[0]} | Total columns: {self.data.shape[1]}\n\n", "stats")
            
            # Data preview
            self.data_msg.insert(tk.END, "Data Preview:\n", "subheader")
            self.data_msg.insert(tk.END, f"{self.data.head().to_string()}\n\n", "data")
            
            # Column info
            self.data_msg.insert(tk.END, "Column Information:\n", "subheader")
            for col in self.data.columns:
                dtype = self.data[col].dtype
                missing = self.data[col].isna().sum()
                missing_pct = (missing / len(self.data)) * 100
                self.data_msg.insert(tk.END, f"• {col}: {dtype} (Missing: {missing} - {missing_pct:.1f}%)\n", "info")
                
            # Tag configuration
            self.data_msg.tag_configure("header", font=("Helvetica", 12, "bold"), foreground="green")
            self.data_msg.tag_configure("subheader", font=("Helvetica", 11, "bold"))
            self.data_msg.tag_configure("stats", font=("Helvetica", 10, "italic"))
            self.data_msg.tag_configure("data", font=("Courier", 9))
            self.data_msg.tag_configure("info", font=("Helvetica", 9))
            
            self.complete_status("Data loaded successfully")
            
        except Exception as e:
            self.data_msg.delete('1.0', tk.END)
            self.data_msg.insert(tk.END, f"❌ Error loading data: {str(e)}")
            self.status.set(f"❌ Error: {str(e)}")
            self.progress.stop()

    def run_eda(self):
        if self.data is None:
            messagebox.showinfo("No Data", "Please load a dataset first.")
            return
            
        self.set_status("Running EDA...")
        
        try:
            self.eda_msg.delete('1.0', tk.END)
            
            # Missing values analysis
            self.eda_msg.insert(tk.END, "Missing Values Analysis:\n", "header")
            missing_data = self.data.isnull().sum()
            missing_percent = (missing_data / len(self.data)) * 100
            missing_df = pd.DataFrame({'Missing Values': missing_data, 
                                       'Percentage': missing_percent})
            self.eda_msg.insert(tk.END, f"{missing_df.to_string()}\n\n", "data")
            
            # Statistical summary
            self.eda_msg.insert(tk.END, "Statistical Summary:\n", "header")
            describe_df = self.data.describe()
            self.eda_msg.insert(tk.END, f"{describe_df.to_string()}\n\n", "data")
            
            # Additional insights
            self.eda_msg.insert(tk.END, "Additional Insights:\n", "header")
            
            # Check for numeric columns
            numeric_cols = self.data.select_dtypes(include=np.number).columns
            if len(numeric_cols) > 0:
                for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
                    self.eda_msg.insert(tk.END, f"• {col}: Min={self.data[col].min():.2f}, Max={self.data[col].max():.2f}, Mean={self.data[col].mean():.2f}\n", "info")
            
            # Tag configuration
            self.eda_msg.tag_configure("header", font=("Helvetica", 12, "bold"))
            self.eda_msg.tag_configure("data", font=("Courier", 9))
            self.eda_msg.tag_configure("info", font=("Helvetica", 10))
            
            # Create correlation heatmap
            self.clear_frame(self.eda_plot_frame)
            
            try:
                # Only select numeric columns for correlation
                num_data = self.data.select_dtypes(include=np.number)
                if len(num_data.columns) > 1:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    
                    # Create mask for upper triangle
                    mask = np.triu(np.ones_like(num_data.corr(), dtype=bool))
                    
                    # Enhanced heatmap
                    sns.set_theme(style="white")
                    cmap = sns.diverging_palette(230, 20, as_cmap=True)
                    
                    sns.heatmap(num_data.corr(), mask=mask, cmap=cmap, 
                                annot=True, fmt='.2f', square=True, linewidths=.5, 
                                cbar_kws={"shrink": .8}, ax=ax)
                    
                    ax.set_title("Correlation Heatmap", fontsize=16, pad=20)
                    plt.tight_layout()
                    
                    self.display_plot(fig, self.eda_plot_frame)
                else:
                    no_data_label = tb.Label(self.eda_plot_frame, 
                                          text="Not enough numeric columns for correlation analysis",
                                          font=("Helvetica", 12))
                    no_data_label.pack(expand=True, pady=50)
            except Exception as e:
                error_label = tb.Label(self.eda_plot_frame, 
                                    text=f"Error creating correlation plot: {str(e)}",
                                    foreground="red")
                error_label.pack(expand=True, pady=50)
            
            self.complete_status("EDA Complete")
            
        except Exception as e:
            self.eda_msg.delete('1.0', tk.END)
            self.eda_msg.insert(tk.END, f"❌ Error in EDA: {str(e)}")
            self.status.set(f"❌ Error: {str(e)}")
            self.progress.stop()

    def visualize_data(self):
        if self.data is None:
            messagebox.showinfo("No Data", "Please load a dataset first.")
            return
            
        self.set_status("Creating visualizations...")
        
        try:
            self.clear_frame(self.viz_plot_frame)
            
            # Get numeric columns for plotting
            numeric_cols = self.data.select_dtypes(include=np.number).columns
            
            if len(numeric_cols) == 0:
                no_data_label = tb.Label(self.viz_plot_frame, 
                                      text="No numeric columns available for visualization",
                                      font=("Helvetica", 12))
                no_data_label.pack(expand=True, pady=50)
                self.complete_status()
                return
                
            plot_type = self.plot_type.get()
            
            if plot_type == "default":
                # Multi-plot visualization
                fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Reduced figure size for better fit
                fig.suptitle("Data Visualization Dashboard", fontsize=16, y=0.98)
                
                # Plot 1: Histogram
                if len(numeric_cols) > 0:
                    # Sample the data if there are too many rows to prevent freezing
                    sample_size = min(1000, len(self.data))
                    sample_data = self.data.sample(sample_size) if len(self.data) > sample_size else self.data
                    
                    sns.histplot(sample_data[numeric_cols[0]], kde=True, ax=axes[0, 0], color="#3498db", bins=20)
                    axes[0, 0].set_title(f"Distribution of {numeric_cols[0]}")
                    axes[0, 0].grid(True, linestyle='--', alpha=0.7)
                
                # Plot 2: Boxplot
                if len(numeric_cols) > 1:
                    sns.boxplot(y=sample_data[numeric_cols[1]], ax=axes[0, 1], color="#2ecc71")
                    axes[0, 1].set_title(f"Boxplot of {numeric_cols[1]}")
                    axes[0, 1].grid(True, linestyle='--', alpha=0.7)
                
                # Plot 3: Violin plot
                if len(numeric_cols) > 2:
                    sns.violinplot(y=sample_data[numeric_cols[2]], ax=axes[1, 0], color="#9b59b6")
                    axes[1, 0].set_title(f"Violin plot of {numeric_cols[2]}")
                    axes[1, 0].grid(True, linestyle='--', alpha=0.7)
                
                # Plot 4: KDE plot
                if len(numeric_cols) > 3:
                    sns.kdeplot(sample_data[numeric_cols[3]], ax=axes[1, 1], fill=True, color="#e74c3c")
                    axes[1, 1].set_title(f"KDE of {numeric_cols[3]}")
                    axes[1, 1].grid(True, linestyle='--', alpha=0.7)
                
                plt.tight_layout()

            elif plot_type == "heatmap":
                # Heatmap visualization with performance improvements
                fig, ax = plt.subplots(figsize=(10, 8))  # Reduced size
                
                # Get numeric columns for correlation - limit to 15 max columns to prevent freezing
                num_data = self.data.select_dtypes(include=np.number)
                if len(num_data.columns) > 15:
                    num_data = num_data.iloc[:, :15]  # Limit to first 15 columns
                    
                # Calculate correlation with smaller data
                corr_data = num_data.corr()
                
                # Create mask for upper triangle
                mask = np.triu(np.ones_like(corr_data, dtype=bool))
                
                # Create heatmap with simpler styling to improve performance
                cmap = sns.diverging_palette(220, 10, as_cmap=True)
                sns.heatmap(corr_data, mask=mask, cmap=cmap, 
                           vmax=1, vmin=-1, center=0, square=True, linewidths=.5, 
                           cbar_kws={"shrink": .8}, 
                           annot=True if len(corr_data) < 10 else False,  # Only show annotations for smaller matrices
                           fmt=".2f", ax=ax)
                
                ax.set_title("Correlation Heatmap", fontsize=16, pad=20)

            elif plot_type == "boxplot":
                # Multiple boxplots with improved sizing
                fig, ax = plt.subplots(figsize=(10, 6))  # Reduced size for better fit
                
                # Get first few numeric columns (limit to prevent performance issues)
                cols_to_plot = numeric_cols[:min(6, len(numeric_cols))]
                
                # Sample the data if there are too many rows
                sample_size = min(1000, len(self.data))
                sample_data = self.data.sample(sample_size) if len(self.data) > sample_size else self.data
                
                plot_data = sample_data[cols_to_plot].melt()
                
                # Create boxplot with updated parameters
                sns.boxplot(x="variable", y="value", data=plot_data, ax=ax, 
                           palette="Set3", width=0.6)  # Changed palette and width
                
                ax.set_title("Boxplots of Numeric Features", fontsize=14, pad=10)
                ax.set_xlabel("Features")
                ax.set_ylabel("Values")
                ax.grid(True, linestyle='--', alpha=0.7)
                plt.xticks(rotation=30)  # Reduced rotation angle
                
                # Better use of space
                plt.tight_layout()
                
            elif plot_type == "histogram":
                # Multiple histograms with performance improvements
                fig = plt.figure(figsize=(9, 6))  # Smaller figure size
                
                # Get first few numeric columns
                cols_to_plot = numeric_cols[:min(4, len(numeric_cols))]
                
                # Sample the data if there are too many rows
                sample_size = min(1000, len(self.data))
                sample_data = self.data.sample(sample_size) if len(self.data) > sample_size else self.data
                
                for i, col in enumerate(cols_to_plot, 1):
                    ax = fig.add_subplot(2, 2, i)
                    
                    # Use fewer bins and no KDE for better performance
                    sns.histplot(sample_data[col], bins=15, kde=False, ax=ax, 
                               color=sns.color_palette("husl", 8)[i-1])
                    
                    ax.set_title(f"Distribution of {col}")
                    ax.grid(True, linestyle='--', alpha=0.7)
                    
                    # Limit the number of ticks for better readability
                    ax.locator_params(axis='x', nbins=5)
                
                plt.tight_layout()
                fig.suptitle("Feature Distributions", fontsize=14, y=0.98)
                
            # Display the plot
            self.display_plot(fig, self.viz_plot_frame)
            self.complete_status("Visualization Complete")
            
        except Exception as e:
            error_label = tb.Label(self.viz_plot_frame, 
                                text=f"❌ Error creating visualization: {str(e)}",
                                foreground="red")
            error_label.pack(expand=True, pady=50)
            self.status.set(f"❌ Error: {str(e)}")
            self.progress.stop()

    def calculate_aqi(self):
        try:
            pm_value = float(self.pm_entry.get())
            
            # AQI calculation (simplified EPA formula)
            if pm_value <= 12.0:
                aqi = linear_scale(pm_value, 0, 12.0, 0, 50)
                level = "Good"
                color = "#00e400"  # Green
                desc = "Air quality is satisfactory, and air pollution poses little or no risk."
            elif pm_value <= 35.4:
                aqi = linear_scale(pm_value, 12.1, 35.4, 51, 100)
                level = "Moderate"
                color = "#ffff00"  # Yellow
                desc = "Air quality is acceptable; however, some pollutants may be a concern for a small number of sensitive individuals."
            elif pm_value <= 55.4:
                aqi = linear_scale(pm_value, 35.5, 55.4, 101, 150)
                level = "Unhealthy for Sensitive Groups"
                color = "#ff7e00"  # Orange
                desc = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
            elif pm_value <= 150.4:
                aqi = linear_scale(pm_value, 55.5, 150.4, 151, 200)
                level = "Unhealthy"
                color = "#ff0000"  # Red
                desc = "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
            elif pm_value <= 250.4:
                aqi = linear_scale(pm_value, 150.5, 250.4, 201, 300)
                level = "Very Unhealthy"
                color = "#99004c"  # Purple
                desc = "Health warnings of emergency conditions. The entire population is more likely to be affected."
            else:
                aqi = linear_scale(pm_value, 250.5, 500.4, 301, 500)
                level = "Hazardous"
                color = "#7e0023"  # Maroon
                desc = "Health alert: everyone may experience more serious health effects."
            
            # Update UI with results
            self.aqi_result.set(f"AQI: {int(aqi)} - {level}")
            self.aqi_desc.set(desc)
            self.aqi_value_label.configure(foreground=color)
            
        except ValueError:
            self.aqi_result.set("Invalid Input")
            self.aqi_desc.set("Please enter a valid number")
            self.aqi_value_label.configure(foreground="red")

    def display_plot(self, fig, frame):
        # Clear previous plot if any
        for widget in frame.winfo_children():
            widget.destroy()
            
        # Apply style to figure
        if self.current_theme == "superhero":
            plt.style.use('dark_background')
            fig.patch.set_facecolor('#2c3e50')
            for ax in fig.get_axes():
                ax.set_facecolor('#34495e')
        else:
            plt.style.use('default')
            
        # Create canvas for the plot
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add toolbar for better interaction
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = tb.Frame(frame)
        toolbar_frame.pack(fill=tk.X, padx=10)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

# Helper function for AQI calculation
def linear_scale(value, low_val, high_val, low_aqi, high_aqi):
    return ((high_aqi - low_aqi) / (high_val - low_val)) * (value - low_val) + low_aqi

if __name__ == "__main__":
    # Set plotting style globally
    plt.style.use('seaborn-v0_8')
    sns.set_theme(style="darkgrid")
    
    # Enable high-res displays support
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 120
    
    # Increase the interactive plotting backend size limit
    mpl.rcParams['agg.path.chunksize'] = 10000
    
    # Create and run the app
    app_root = tb.Window(themename="superhero")
    app = AirWiseApp(app_root)
    app_root.mainloop()
