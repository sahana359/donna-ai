//
//  Message.swift
//  ui
//
//  Created by Sahana Rajashekara on 2/9/26.
//

import Foundation

struct Message: Identifiable {
    let id: UUID
    let content: String
    let isFromUser: Bool
    let timestamp: Date
    
    init(content: String, isFromUser: Bool) {
        self.id = UUID()
        self.content = content
        self.isFromUser = isFromUser
        self.timestamp = Date()
    }
}
