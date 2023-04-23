# IEC62443 Framework Mapping Controls to MITRE ATT&CK

I was thinking how I do the mapping between IEC62443-3-3 controls series and IEC62443-4-2 to MITRE ATT&CK TTPs as well as ICS TTPs by hand one day. Then I remembered I can use the horse power of OpenAI ChatGPT to do the first heavy lifting and generate a baseline excel file for me first.

Then I can review the baseline and add/subtract wording and ensure it is done the right job. By no means it would be able to do this task accurately, but at a bare minimum can do the original work, and perhaps I can fill the gaps.

So, I wrote this code to make it happen.

## Input

The input is an excel file with all controls (SL1-4) as rows of an excel file. My specific excel had two sheets:

- Sheet 1: System level requirements is for IEC62443-3-3 System Requirements with all the requirements for all levels listed in rows.
- Sheet 2: Componenet level requirements is for IEC62443-4-2 Component Requirements with all the requirements including EDRs, NDR, HDR and SAR requirements.

The excel file had a heading with columns named as:
- Clause: The Foundational Requirement Text, 
- Control Name: The title and number of controls
- Control Text: The actual text of the control.

* Rows that had text of Foundational Requirements (FR) and their description was just for segregating the controls for readability of excel. That's why the code was ignoring them and jump over these entries. 
* 

## Output

The output is just the same excel file, but with the corresponding responses of ChatGPT to each control for Tactics, Techniques. I also wanted the code to generate a "Verification Instruction" for each control. Who knows, it might become useful in future projects or specific circumstances.

