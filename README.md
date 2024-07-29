# AFM-Analyser


AFM-Analyser, görüntü işleme ve kullanıcı arayüzü uygulamasıdır. Bu uygulama, OpenCV, Tkinter ve diğer kütüphaneleri kullanarak çeşitli görüntü işleme görevlerini gerçekleştirir.

## Özellikler

- Görüntü yükleme ve görüntüleme
- Görüntü işlemleri (örneğin, gri tonlama, bulanıklaştırma)
- Çıktıları kaydetme

## Gereksinimler

- Python 3.10 veya üstü
- Aşağıdaki Python paketleri:
  - opencv-python
  - numpy
  - matplotlib
  - pillow

## Kurulum

1. Bu projeyi klonlayın:

    ```sh
    git clone https://github.com/coderasnoise/AFM-Analyser.git
    cd AFM-Analyser
    ```

2. Bir sanal ortam oluşturun ve etkinleştirin:

    ```sh
    python -m venv venv
    source venv/bin/activate  # Windows için: venv\Scripts\activate
    ```

3. Gerekli paketleri yükleyin:

    ```sh
    pip install -r requirements.txt
    ```

## Kullanım

1. Ana Python dosyasını çalıştırın:

    ```sh
    python app.py
    ```

2. PyInstaller ile EXE dosyası oluşturmak için:

    ```sh
    pyinstaller --onefile --windowed --hidden-import=cv2 --hidden-import=numpy --hidden-import=matplotlib --hidden-import=tkinter app.py
    ```


