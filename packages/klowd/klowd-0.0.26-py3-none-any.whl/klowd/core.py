from typing import Any
import anywidget
import json
import pyodide
import traitlets

config = {}

class GrantToken(anywidget.AnyWidget):
    _esm = """\
    function render({ model, el }) {
      const container = document.createElement("div");
      container.classList.add("kloud-confirm-container");
    
      const questionDiv = document.createElement("div");
      questionDiv.innerHTML = 'Скрипт запрашивает доступ к платформе. Разрешить?';
      questionDiv.classList.add("kloud-confirm-question");
      
      const okButton = document.createElement("button");
      okButton.classList.add("kloud-confirm-button");
      okButton.innerHTML = 'Разрешить';
      okButton.addEventListener("click", () => {
        model.set("value", sessionStorage.getItem('kloud_token'));
        model.save_changes();
      });
      container.appendChild(questionDiv);
      container.appendChild(okButton);
      el.appendChild(container);
      model.on("change:value", () => {
        if (!model.get("value")) return;
        questionDiv.innerHTML = "Доступ предоставлен";
        container.removeChild(okButton);
        container.style.borderColor = "green";
      });
    }
	export default { render };
    """
    _css = """\
        .kloud-confirm-container {
            align-items: center;
            border: 5px solid var(--jp-rendermime-error-background);
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            font-size: 20px;
            gap: 20px;
            padding: 20px;
        }
        .kloud-confirm-question {
            color: var(--jp-content-font-color1);
            opacity: 0.9;
        }
        
        .kloud-confirm-button {
            background: #72584b;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-size: 20px;
            opacity: 0.8;
            padding: 10px 20px;
        }
    """
    value = traitlets.Unicode('').tag(sync=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        display(self)

class Drive:
    kloudUrl=None
    kloud_token=None
    
    def grant_access(self, kloudUrl=""):
        self.kloudUrl = kloudUrl
        self.kloud_token = GrantToken()

    @property
    def token(self):
        return self.kloud_token.value
    
    async def fetch(self, url, **kwargs):
        if self.kloud_token is None:
            raise PermissionError('Доступ в drive.grant_access() не предоставлен')

        headers = {'Authorization': f'Bearer {self.token}'}
        
        modified_kwargs = kwargs
        if 'headers' in modified_kwargs:
            headers.update(kwargs['headers'])
            del modified_kwargs['headers']

        return await pyodide.http.pyfetch(f'{self.kloudUrl}{url}', **modified_kwargs, headers=headers)
    
    async def getBlob(self, blobId, revision=0):
        url = '/api/Storage/Remote/Blobs/Download/Token'
        response = await self.fetch(
            url,
            body=json.dumps({
                'fileBlobs': [{
                    'name': 'data',
                    'id': blobId,
                    'revision': revision,
                }]
            }),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            method='POST'
        )
        if not response.ok:
            raise ConnectionError('Не удалось получить данные')
        
        downloadToken = json.loads(await response.text())
        response = await self.fetch(f'/api/Storage/Remote/Blobs/Download?token={downloadToken}')
        if not response.ok:
            raise ConnectionError('Не удалось получить данные')
        return await response.bytes()




drive = Drive()
