
import face_recognition
import cv2
import os
import time



# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
known_face_encoding_array = []


# Load a sample picture and learn how to recognize it.
list_files = os.listdir("known")
print "Learning about  registered users faces ...."
for file_name in list_files:
	if  file_name.endswith(".png") or file_name.endswith(".jpg") :
		print file_name.split('.')[0]
		file_name_abs = "./known/" + file_name
	known_image = face_recognition.load_image_file(file_name_abs)
	known_face_encoding = face_recognition.face_encodings(known_image)[0]
	known_face_encoding_array.append((known_face_encoding,file_name))


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
count = 0

print "Starting the camera now ...."
while True:
    # Grab a single frame of video
	ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
	if process_this_frame:
		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(small_frame)
		face_encodings = face_recognition.face_encodings(small_frame, face_locations)

	face_names = []
	for face_encoding in face_encodings:
	# See if the face is a match for the known face(s)
		name = "Unknown"
		for known_face_enc, file_name in known_face_encoding_array:
			match = face_recognition.compare_faces([known_face_enc], face_encoding)
			if match[0]:
				name = file_name
				process_this_frame = False
				count = 0
		face_names.append(os.path.splitext(name)[0])

	if count%30 == 0:
		process_this_frame = True

	if count==50:
		x.write(not litup)
		y.write(not litup)
		count = 0
		count = count + 1
	print count

    # Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
        	# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
	cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
