# CameraSensor

Project to work with a Camera connected to a Rpi in python.
Calibration

Pattern Detection &

Real-Time face recognition


Phases of the project 

Nuestro proyecto será un repaso integral a lo visto durante el curso. En primer lugar , vamos a establecer una contraseña a modo de colores predominantes en una imagen. Nuestra contraseña para poder seguir con el juego será la siguiente : 


Rojo , Azul , Negro , Azul

De maner que si le presentamos a nuestra camara estos colores de manera predominante en ese determinado orden , el juego se desbloqueará. Cualquier otra combinación no será válida. 

En primer lugar, con ayuda de los conocimientos adquiridos a lo largo del curso, hemos realizado una calibración estándar y hemos usado para ello un tablón de ajedrez. Nos hemos guardado las imágenes en la ruta imágenes_calibración. Para la calibración nos hemos ayudado de la función find Chessboard corners de cv2

Desbloqueo de contraseña: 
Cada vez que detecta uno de los colores , mostrará por pantalla el resultado , para que puedas proceder a realizar el sguiente frame. Se mostrará este mensaje se esté introduciendo la secuencia correcta o no. Se pedirá un input para pasar de un frame a otro ya que en real time podría ser un lío y no nos enteramos si estamos introduciendo bien o no la secuencia


Tracking desbloqueado 

En el caso de introducir la contraseña de manera correcta, se desbloquea un tracker, que detecta caras en tiempo real. La pantalla mostrará la imagen que detecta la cámara y un cuadriculo alrededor de todas las caras humanas que se presenten delante de ella. Para este tracker , nos hemos ayudado de una arrchivo xml (que está específicamente diseñado con los parámetros de una cara humana de cara a la librería cv2. 
