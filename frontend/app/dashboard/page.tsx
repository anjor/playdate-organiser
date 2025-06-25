'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { format } from 'date-fns';
import api from '@/lib/api';
import { Playdate } from '@/types';

export default function DashboardPage() {
  const [playdates, setPlaydates] = useState<Playdate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPlaydates();
  }, []);

  const fetchPlaydates = async () => {
    try {
      const response = await api.get('/playdates');
      setPlaydates(response.data);
    } catch (error) {
      console.error('Failed to fetch playdates:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="px-4 sm:px-0">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Available Playdates</h1>
          <p className="mt-2 text-sm text-gray-700">
            Browse available playdates in your area
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <Link
            href="/dashboard/create-playdate"
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
          >
            Create Playdate
          </Link>
        </div>
      </div>

      {playdates.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No playdates available yet.</p>
          <p className="text-gray-500 mt-2">Be the first to create one!</p>
        </div>
      ) : (
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {playdates.map((playdate) => (
            <div
              key={playdate.id}
              className="bg-white overflow-hidden shadow rounded-lg"
            >
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg font-medium text-gray-900">{playdate.title}</h3>
                <p className="mt-1 text-sm text-gray-500">{playdate.description}</p>
                <div className="mt-4 space-y-2">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Date:</span>{' '}
                    {format(new Date(playdate.date_time), 'PPP')}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Time:</span>{' '}
                    {format(new Date(playdate.date_time), 'p')}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Location:</span> {playdate.location}
                  </p>
                </div>
                <div className="mt-5">
                  <Link
                    href={`/dashboard/playdates/${playdate.id}`}
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    View details →
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}