#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <opencv2/opencv.hpp>

using namespace cv;

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <IP_ADDRESS> <PORT>\n", argv[0]);
        return 1;
    }

    const char *ip = argv[1];
    int port = atoi(argv[2]);

    // Initialize socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip, &server_address.sin_addr);

    // Initialize OpenCV
    VideoCapture cap(0); // Open the default camera
    if (!cap.isOpened()) {
        fprintf(stderr, "Could not open video capture.\n");
        return 1;
    }

    int frameCount = 0;
    while (1) {
        Mat frame;
        cap >> frame;

        if (frame.empty()) {
            fprintf(stderr, "Empty frame.\n");
            break;
        }

        if (frameCount % 2 == 0) { // Send every other frame
            // Serialize Mat object
            std::vector<uchar> buffer;
            imencode(".jpg", frame, buffer);

            // Send buffer over RTP (Note: This is a simplified example and not a real RTP packet)
            sendto(sock, &buffer[0], buffer.size(), 0, (struct sockaddr *)&server_address, sizeof(server_address));
        }

        frameCount++;
        usleep(30000); // Sleep for 30 ms
    }

    close(sock);
    return 0;
}
