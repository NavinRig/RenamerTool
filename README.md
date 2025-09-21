# RenamerTool
 The Maya Renamer Tool is a lightweight, user-friendly Python tool for Autodesk Maya that allows you to batch rename objects in your scene quickly and consistently.
 It is designed to streamline naming workflows in production environments, helping artists maintain clean and organized scene hierarchies

![RenamerTool](https://github.com/user-attachments/assets/6146a115-83f1-400c-ab92-62fba313d5e1)

# Key Features
- Batch Rename – Select multiple objects and rename them in one go.
- Custom Prefix/Suffix – Add custom text to the start or end of object names.
- Search & Replace – Find specific substrings in names and replace them with new text.
- Automatic Numbering / Padding – Adds numeric suffixes with support for padded numbering (e.g., _01, _002).
- Alphabetical Increment Support – After Z, tool automatically continues with AA, AB, etc.
- Undo-Friendly – All operations are undoable within Maya.
- Simple UI – Easy-to-use interface

# UI Features
- Base Name Field: Enter a custom name for objects.
- Prefix/Suffix Fields: Quickly add pipeline-specific identifiers.
- Padding Control: Choose how many digits to pad (1, 2, 3...).
- Preview Mode: Shows a preview of final names before committing.
- Rename Button: One-click execution.

# Technical Details
- Language: Python
- Compatibility: Maya 2020+, tested up to Maya 2026
