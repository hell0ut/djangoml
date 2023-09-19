FROM python:3.10

RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
	  apt install -y git && \
	  apt install -y vim && \
	  apt install -y gcc
	#   git clone --depth=1 https://github.com/amix/vimrc.git ~/.vim_runtime && \
	#   sh ~/.vim_runtime/install_awesome_vimrc.sh && \
	#   sh -c "$(wget -O- https://raw.githubusercontent.com/deluan/zsh-in-docker/master/zsh-in-docker.sh)"

COPY requirements_copy.txt requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
RUN pip3 install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY yolo_backend/ .

LABEL maintainer="Vladyslav Poplavskyi <vlad.poplavskyi@gmail.com>"

CMD ./scripts/start_fixed.sh