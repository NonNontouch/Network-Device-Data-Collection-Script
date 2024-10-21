main_style = """
#main_bg_color {
    background-color: #4D4D4D;
}

#input_label {
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    background-color: #5C5C5C; 
    color: white;
    font-weight: bold;
}

#enable_pass_label {
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    background-color: #5C5C5C;
    font-size: 18px;
    color: white;
}

#input_lineedit {
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    min-width: 200px;
    background-color: #4D4D4D;
    color: white;
}

#connection_grid_label {
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    background-color: #696969;
    color: white;
}

#popup_dialog_button {
    background-color: #4CAF50;
    color: white;
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 20px;
}

#popup_dialog_button:hover {
    background-color: #45a049;
}

#popup_dialog_button:pressed {
    background-color: #388E3C;
}
#createCommandButton {
    background-color: #1E90FF;  
    color: white; 
    border: 2px solid #1E90FF;
    border-radius: 10px;  
    padding: 10px 20px; 
    font-size: 16px;
}

#createCommandButton:hover {
    background-color: #1C86EE;  
    border-color: #1C86EE;  
}

#createCommandButton:active {
    background-color: #1874CD; 
    border-color: #1874CD; 
}
#input_widget {
    background-color: #252525;
    border: 2px solid black;
    border-radius: 10px;
    color: white;
}

#sub_input_widget {
    background-color: #4D4D4D;
    border-radius: 10px;
    border: 2px solid black;
    padding: 10px;
}

#input_label_configure_dialog {
    border: 2px solid black;
    border-radius: 10px;
    padding: 3px;
    color: white;
    background-color: #5C5C5C;
    font: 16px;
    min-width: 160px
}

#input_lineedit_configure_dialog {
    border: 2px solid black;
    border-radius: 10px;
    padding: 3px;
    min-width: 200px;
    color: white;
    background-color: #4D4D4D;
    font-size: 16px;
}

#label_banner {
    font-size: 18px;
    font-weight: bold;
    color: white;
    padding: 10px;
    background-color: #4D4D4D;
    border-radius: 10px;
    text-align: center;
}

#acceptButton {
    background-color: #4CAF50;
    color: white;
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#acceptButton:hover {
    background-color: #45a049;
}

#acceptButton:pressed {
    background-color: #388E3C;
}

#cancelButton {
    background-color: #f44336;
    color: white;
    border: 2px solid #f44336;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#cancelButton:hover {
    background-color: #e53935;
}

#cancelButton:pressed {
    background-color: #c62828;
}

#createJsonButton {
    background-color: #4CAF50;
    color: white;
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#createJsonButton:hover {
    background-color: #45a049;
}

#createJsonButton:pressed {
    background-color: #388E3C;
}

#createOSVersionButton {
    background-color: #2196F3;
    color: white;
    border: 2px solid #2196F3;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#createOSVersionButton:hover {
    background-color: #1976D2;
}

#createOSVersionButton:pressed {
    background-color: #1565C0;
}

#deleteButton {
    background-color: #f44336;
    color: white;
    border: 2px solid #f44336;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#deleteButton:hover {
    background-color: #e53935;
}

#deleteButton:pressed {
    background-color: #c62828;
}

#activeCheckbox {
    spacing: 5px;
    color:white;
}

#activeCheckbox::indicator {
    width: 20px;
    height: 20px;
}

#activeCheckbox::indicator:unchecked {
    background-color: #f44336;
    border: 2px solid #c62828;
    border-radius: 3px;
}

#activeCheckbox::indicator:checked {
    background-color: #4CAF50;
    border: 2px solid #388E3C;
}

#activeCheckbox::indicator:checked:hover {
    background-color: #45a049;
}

#activeCheckbox::indicator:unchecked:hover {
    border: 2px solid #e53935;
}


QToolTip {
    background-color: #333333;  /* Dark background */
    color: white;  /* White text */
    border: 1px solid #4CAF50;  /* Optional: green border to match the icon */
    padding: 5px;  /* Padding for better readability */
    font-size: 14px;  /* Set the font size */
}

#result_button_preview {
    background-color: #2196F3;
    color: white;
    border: 2px solid #2196F3;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#result_button_preview:hover {
    background-color: #1976D2;
}

#result_button_preview:pressed {
    background-color: #1565C0;
}

#result_button_save_image {
    background-color: #FFA500;
    color: white;
    border: 2px solid #2196F3;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#result_button_save_image:hover {
    background-color: #FF8C00;
}

#result_button_save_image:pressed {
    background-color: #FF7F00;
}

#result_button_save_text {
    background-color: #ADD8E6;
    color: black;
    border: 2px solid #ADD8E6;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#result_button_save_text:hover {
    background-color: #87CEEB;
}

#result_button_save_text:pressed {
    background-color: #00BFFF;
}

#single_result_widget {
    background-color: #2C3E50;
    border: 4px solid #1F2A35; 
    border-radius: 10px;
    color: white;
    padding: 10px;
}

QScrollArea {
    background-color: #252525; 
    border: 2px solid #4D4D4D; 
    border-radius: 10px;       
}

QScrollBar:vertical {
    border: 2px solid #4D4D4D;
    background: #4D4D4D;      
    width: 15px;              
    margin: 22px 0 22px 0;    
}

QScrollBar::handle:vertical {
    background: #888888;     
    min-height: 20px;        
    border-radius: 7px;      
}

QScrollBar::handle:vertical:hover {
    background: #555555;      
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;         
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;         
}

QScrollBar:horizontal {
    border: 2px solid #4D4D4D; 
    background: #4D4D4D;       
    height: 15px;              
    margin: 0 22px 0 22px;     
}

QScrollBar::handle:horizontal {
    background: #888888;    
    min-width: 20px;        
    border-radius: 7px;     
}

QScrollBar::handle:horizontal:hover {
    background: #555555;     
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: none;        
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;        
}
#debug_textedit{
    background-color: #252525;
    color: white;
    border: 2px solid #4D4D4D;
    border-radius: 10px;
    padding: 5px;
}
#debug_textedit:focus{
    border: 2px solid #888888; 
}
#loading_label{
    color: white; 
    font-size: 16px; 
    background-color: #4D4D4D;
}
#loading_progress{
    background-color: #252525; 
    border: 2px solid #4D4D4D; 
    border-radius: 10px;
    text-align: center; 
}
#loading_progress:chunk {
    background-color: #4CAF50;
    border-radius: 10px;
}
#warning_result_widget {
    background-color: #FFA500;
    border: 2px solid black;  
    border-radius: 10px;      
    color: black;             
}

#danger_result_widget {
    background-color: #FF4500;
    border: 2px solid black;  
    border-radius: 10px;      
    color: white;             
}

#result_widget_error {
    background-color: #DC143C;
    border: 2px solid black;
    border-radius: 10px;
   }
#edit_connection_variable_button {
    background-color: #FFA500;
    color: white;
    border: 2px solid #FFA500;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#edit_connection_variable_button:hover {
    background-color: #FF8C00;
}

#edit_connection_variable_button:pressed {
    background-color: #FF7F00;
}
#open_debug_window_button {
    background-color: #ADD8E6;
    color: black;
    border: 2px solid #ADD8E6;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#open_debug_window_button:hover {
    background-color: #87CEEB;
}

#open_debug_window_button:pressed {
    background-color: #00BFFF;
}
#edit_os_template_button {
    background-color: #2196F3;
    color: white;
    border: 2px solid #2196F3;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#edit_os_template_button:hover {
    background-color: #1976D2;
}

#edit_os_template_button:pressed {
    background-color: #1565C0;
}
#info_icon {
    background-color: transparent;
    color: #4CAF50;
    border: none;
    font-size: 20px;
}

#info_icon:hover .info_popup {
    display: block;
}
#save_all_image_button {
    background-color: #8A2BE2;
    color: white;
    border: 2px solid #8A2BE2;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#save_all_image_button:hover {
    background-color: #7A1FCB;
}

#save_all_image_button:pressed {
    background-color: #6A0FB0;
}
#save_all_text_button {
    background-color: #20B2AA;
    color: white;
    border: 2px solid #20B2AA;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

#save_all_text_button:hover {
    background-color: #1B9E95;
}

#save_all_text_button:pressed {
    background-color: #17857E;
}
    """
