//
//  ChatService.swift
//  ui
//
//  Created by Sahana Rajashekara on 2/9/26.
//

import Foundation

struct ChatService {
    let baseURL: String
    
    struct ChatRequest: Codable {
        let message: String
    }
    
    struct ChatResponse: Codable {
        let text: String
    }
    
    func send(message: String) async throws -> String {
        guard let url = URL(string: "\(baseURL)/chat") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ChatRequest(message: message)
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        
        let chatResponse = try JSONDecoder().decode(ChatResponse.self, from: data)
        return chatResponse.text
    }
}
