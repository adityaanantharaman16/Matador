import Foundation

struct Notification: Identifiable {
    let id: UUID                  // Unique identifier for the notification
    let user: User                // The user who triggered the notification
    let content: String           // Content of the notification (e.g., "Sarah liked your pitch")
    let createdAt: Date           // When the notification was created
    let isRead: Bool              // Whether the notification has been read
    let type: NotificationType    // Type of notification (like, comment, follow)
}

enum NotificationType {
    case like
    case comment
    case follow
}
