//
//  MessageBubble.swift
//  ui
//
//  Created by Sahana Rajashekara on 2/9/26.
//

import SwiftUI

struct MessageBubble: View {
    let message: Message
    
    var body: some View {
        HStack {
            if message.isFromUser { Spacer() }
            
            Text(message.content)
                .padding(12)
                .background(message.isFromUser ? Color.blue : Color.gray.opacity(0.3))
                .foregroundColor(message.isFromUser ? .white : .primary)
                .cornerRadius(16)
            
            if !message.isFromUser { Spacer() }
        }
    }
}

#Preview {
    VStack {
        MessageBubble(message: Message(content: "Hey there!", isFromUser: false))
        MessageBubble(message: Message(content: "Hi! How's it going?", isFromUser: true))
    }
    .padding()
}
