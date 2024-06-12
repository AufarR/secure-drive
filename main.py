import flet as ft
from rc4 import rc4
from os import getcwd

async def main(page: ft.Page):

    # Handlers

    async def handleCipher(e:ft.FilePickerResultEvent):
        try:
            with open(fileInfo.data["path"], "rb") as f:
                text = f.read()
            key = bytes(keyInput.value,'utf-8')
            res = rc4(text,key)
            with open(e.path, "wb") as f:
                f.write(res)
        except Exception as err:
            await alert("Error: " + err.args[0])
        else:
            await alert("File saved as " + e.path)
            fileInfo.data.clear()
            fileInfo.value = "No file selected"
            submitButton.disabled = "path" not in fileInfo.data
            fileInfo.update()
            submitButton.update()
    
    async def fileSelected(e:ft.FilePickerResultEvent):
        fileInfo.value = e.files[0].name
        fileInfo.data["path"] = e.files[0].path
        fileInfo.data["encrypted"] = fileInfo.value.endswith(".enc")
        submitButton.disabled = "path" not in fileInfo.data
        submitButton.text = "Decrypt" if fileInfo.data["encrypted"] else "Encrypt"
        fileInfo.update()
        submitButton.update()
    
    async def alert(msg):
        page.snack_bar.content = ft.Text(msg)
        page.snack_bar.open = True
        page.update()
    
    # Components
    
    filePicker = ft.FilePicker(on_result=fileSelected)
    savePicker = ft.FilePicker(on_result=handleCipher)
    page.overlay.append(filePicker)
    page.overlay.append(savePicker)

    keyInput = ft.TextField(label="Key", password=True, can_reveal_password=True)

    filePick = ft.FilledButton("Select a file", on_click= lambda _: filePicker.pick_files(dialog_title="Select file to encrypt/decrypt"))
    fileInfo = ft.Text("No file selected", data={})

    submitButton = ft.FilledButton(text="Encrypt/Decrypt", disabled=True, on_click= lambda _: savePicker.save_file(
        dialog_title="Select save location",
        file_name= fileInfo.value[:-4] if fileInfo.data["encrypted"] else (fileInfo.value + ".enc")
    ))

    # Main content
    content = ft.SafeArea (
        ft.Container (
            ft.Column(
                [
                    ft.Text("Secure Drive",size=36),
                    ft.Divider(),
                    ft.Container(height=10),
                    ft.Row(
                        [filePick, fileInfo],
                        alignment = ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(height=5),
                    keyInput,
                    ft.Container(height=5),
                    submitButton
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            )
        )
    )

    page.add(content)
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.snack_bar = ft.SnackBar(content=[])


ft.app(target=main)