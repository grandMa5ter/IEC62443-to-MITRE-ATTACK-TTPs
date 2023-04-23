import openai
import pandas as pd
from dotenv import load_dotenv
import sys
import os


# Set up the OpenAI API client
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(device, control, instruction_type):

    if instruction_type == 'tactics':
        system_content = f"You are an assistant of grandMaster, helping him to come up with relevant MITRE ATTACK TTPs and MITRE ATTACK ICS Specific for each of IEC62443 framework requirements."
        user_content = f"In the context of this IEC62443 Framework control: '{control}', can you suggest specific MITRE ATTACK Tactics and ICS tactics as list of tactics that this control is relevant to?"
    elif instruction_type == 'techniques':
        system_content = f"You are an assistant of grandMaster, helping him to come up with relevant MITRE ATTACK TTPs and MITRE ATTACK ICS Specific for each of IEC62443 framework requirements."
        user_content = f"In the context of this IEC62443 Framework control: '{control}', and MITRE ATTACK Tactics you have suggested before, can you suggest MITRE ATTACK Techniques & ATTACK ICS Specific techniques as list of techniques that this control is relevant to? clearly identify ICS specific ones as well in the list."
    else:  # verification
        system_content = f"You are an assistant of grandMaster, helping him to come up with relevant verifications steps required to verify each of IEC62443 framework controls in real world system engineering verification and validation. We are writing Test Procedures for these controls."
        user_content = f"In the context of this IEC62443 Framework control: '{control}', generate verification instructions as a list, step by step for specific device or OS: '{device}'. "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        max_tokens=900,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print(response['choices'][0]['message']['content'].strip())
    return response['choices'][0]['message']['content'].strip()

def process_controls(df, devices):
    # Add new columns to store generated results
    df['Tactics'] = ''
    df['Techniques'] = ''

    for index, row in df.iterrows():
        clause = row['Clause']
        control_name = row['Control Name']
        control_text = row['Control Text']

        # Skip rows with Foundational Requirement text only (no Control Name)
        if pd.isna(control_name):
            continue

        #print(f"Clause: {clause}\nControl Name: {control_name}\nControl Text: {control_text}\n")

        control = control_name + " - " + control_text
        print(f"*************** Sending control : {control_name} ***************\n")
        print("*************** TACTICS ***************\n")
        tactics = generate_answer(None, control, 'tactics')
        print("*************** TECHNIQUES ***************\n")
        techniques = generate_answer(None, control, 'techniques')
        df.at[index, 'Tactics'] = tactics
        df.at[index, 'Techniques'] = techniques

        for device in devices:
            print("*************** Verification Instruction ***************\n")
            verification = generate_answer(device, control, 'verification')
            df.at[index, f'Verification Inst ({device})'] = verification

    return df


def main():
    # Check if the file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python generate_ttp_ver.py <path_to_excel_file>")
        exit(1)

    # Get the file path from the command-line argument
    file_path = sys.argv[1]

    system_df = pd.read_excel(file_path, sheet_name='system', engine='openpyxl')
    component_df = pd.read_excel(file_path, sheet_name='component', engine='openpyxl')

    devices = ['Workstation running Windows', 'PLC', 'RTU', 'Network Device']

    # Process the 'system' sheet
    print("Processing 'system' sheet:")
    system_df = process_controls(system_df, devices)

    # Process the 'component' sheet
    print("Processing 'component' sheet:")
    component_df = process_controls(component_df, devices)

    # Save the updated DataFrames to the original Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        system_df.to_excel(writer, sheet_name='system', index=False)
        # component_df.to_excel(writer, sheet_name='component', index=False)

if __name__ == '__main__':
    main()