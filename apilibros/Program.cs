using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Threading.Tasks;
using System.Text.Json; // Asegúrate de agregar esta directiva

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddCors();

builder.WebHost.UseUrls("http://0.0.0.0:4000");

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors(policy => policy
    .AllowAnyOrigin()
    .AllowAnyHeader()
    .AllowAnyMethod()
    .WithExposedHeaders("Content-Type")
    .WithExposedHeaders("Authorization")
);

app.MapGet("/recommendations", async ([FromQuery] string keyword) =>
{
    if (string.IsNullOrEmpty(keyword))
    {
        return Results.BadRequest("Keyword parameter is required.");
    }

    try
    {
        using var httpClient = new HttpClient();
        var response = await httpClient.GetAsync($"http://localhost:5000/recommendations?keyword={keyword}");

        if (response.IsSuccessStatusCode)
        {
            var jsonResponse = await response.Content.ReadAsStringAsync();
            // Parse JSON response to ensure it's valid JSON
            var recommendations = JsonSerializer.Deserialize<object>(jsonResponse);
            return Results.Json(recommendations);
        }
        else
        {
            var errorMessage = await response.Content.ReadAsStringAsync();
            return Results.BadRequest($"Error from Flask API: {errorMessage}");
        }
    }
    catch (HttpRequestException ex)
    {
        return Results.BadRequest($"Request error: {ex.Message}");
    }
});

app.Run();


