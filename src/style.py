main_style = """
#main_bg_color {
    background-color: #4D4D4D;
}

#input_label {
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    background-color: #4D4D4D;
    color: white;
}

#enable_pass_label {
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    background-color: #4D4D4D;
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
    /* Green background */
    color: white;
    /* White text */
    border: 2px solid #4CAF50;
    /* Green border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#popup_dialog_button:hover {
    background-color: #45a049;
    /* Darker green on hover */
}

#popup_dialog_button:pressed {
    background-color: #388E3C;
    /* Even darker green on press */
}
#createCommandButton {
    background-color: #4CAF50; /* Green background */
    color: white; /* White text */
    border: 2px solid #4CAF50; /* Green border */
    border-radius: 10px; /* Rounded corners */
    padding: 10px 20px; /* Padding inside the button */
    font-size: 16px; /* Font size */
}

#createCommandButton:hover {
    background-color: #45a049; /* Darker green on hover */
}

#createCommandButton:active {
    background-color: #388E3C; /* Even darker green on press */
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
    background-color: #4D4D4D;
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
    /* Light green background */
    color: white;
    /* White text */
    border: 2px solid #4CAF50;
    /* Green border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#acceptButton:hover {
    background-color: #45a049;
    /* Darker green on hover */
}

#acceptButton:pressed {
    background-color: #388E3C;
    /* Even darker green on press */
}

#cancelButton {
    background-color: #f44336;
    /* Light red background */
    color: white;
    /* White text */
    border: 2px solid #f44336;
    /* Red border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#cancelButton:hover {
    background-color: #e53935;
    /* Darker red on hover */
}

#cancelButton:pressed {
    background-color: #c62828;
    /* Even darker red on press */
}

#createJsonButton {
    background-color: #4CAF50;
    /* Light green background */
    color: white;
    /* White text */
    border: 2px solid #4CAF50;
    /* Green border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#createJsonButton:hover {
    background-color: #45a049;
    /* Darker green on hover */
}

#createJsonButton:pressed {
    background-color: #388E3C;
    /* Even darker green on press */
}

#createOSVersionButton {
    background-color: #2196F3;
    /* Light blue background */
    color: white;
    /* White text */
    border: 2px solid #2196F3;
    /* Blue border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#createOSVersionButton:hover {
    background-color: #1976D2;
    /* Darker blue on hover */
}

#createOSVersionButton:pressed {
    background-color: #1565C0;
    /* Even darker blue on press */
}

#deleteButton {
    background-color: #f44336;
    /* Light red background */
    color: white;
    /* White text */
    border: 2px solid #f44336;
    /* Red border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#deleteButton:hover {
    background-color: #e53935;
    /* Darker red on hover */
}

#deleteButton:pressed {
    background-color: #c62828;
    /* Even darker red on press */
}

#activeCheckbox {
    spacing: 5px;
    /* Space between the checkbox and the label */
}

#activeCheckbox::indicator {
    width: 20px;
    /* Width of the checkbox */
    height: 20px;
    /* Height of the checkbox */
}

#activeCheckbox::indicator:unchecked {
    background-color: #f44336;
    /* Red background for unchecked state */
    border: 2px solid #c62828;
    /* Darker red border for unchecked state */
    border-radius: 3px;
    /* Slightly rounded corners for a modern look */
}

#activeCheckbox::indicator:checked {
    background-color: #4CAF50;
    /* Light green background for checked state */
    border: 2px solid #388E3C;
    /* Darker green border for checked state */
}

#activeCheckbox::indicator:checked:hover {
    background-color: #45a049;
    /* Darker green on hover when checked */
}

#activeCheckbox::indicator:unchecked:hover {
    border: 2px solid #e53935;
    /* Darker red border on hover when unchecked */
}


QToolTip {
    font-size: 16px;
    /* Smaller font size */
    padding: 5px;
    /* Adjust padding */
    background-color: #4D4D4D;
    /* Background color */
    color: white;
    /* Text color */
}

#result_button_preview {
    background-color: #2196F3;
    /* Sky blue background */
    color: white;
    /* White text */
    border: 2px solid #2196F3;
    /* Sky blue border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#result_button_save_image {
    background-color: #FFA500;
    /* orange background */
    color: white;
    /* White text */
    border: 2px solid #2196F3;
    /* orange border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#result_button_save_text {
    background-color: #ADD8E6;
    /* light blue background */
    color: black;
    /* White text */
    border: 2px solid #ADD8E6;
    /* light blue border */
    border-radius: 10px;
    /* Rounded corners */
    padding: 10px 20px;
    /* Padding inside the button */
    font-size: 16px;
    /* Font size */
}

#single_result_widget {
    background-color: #252525;
    border: 2px solid black;
    border-radius: 10px;
    color: white;
}

#result_widget_error {
    background-color: #DC143C;
    border: 2px solid black;
    border-radius: 10px;
    color: white;
}
    """
