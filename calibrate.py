from Robot import Robot

bot = Robot()
speed = 80  # Keep this constant for all tests
duration = 3.0 # Seconds

print(f"Starting calibration: {speed} speed for {duration} seconds...")

# Drive forward at above speed for above duration
bot.drive_forward_timed(speed, duration)

print("Test complete. Measure the distance traveled!")
